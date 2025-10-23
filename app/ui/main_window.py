from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QToolBar,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
)

from app.core.plugin_loader import load_plugin
from app.core.recognizer import Prediction, BaseRecognizer
from app.core.video import VideoCaptureWorker, VideoThread, Roi


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(QSize(480, 360))
        self.setStyleSheet("background-color: #111; border: 1px solid #333;")

    def update_image(self, frame_bgr: np.ndarray) -> None:
        h, w = frame_bgr.shape[:2]
        img_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        qimg = QImage(img_rgb.data, w, h, w * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qimg)
        self.setPixmap(pix.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Language to Text")
        self.setMinimumSize(1100, 700)

        self.recognizer: Optional[BaseRecognizer] = None
        self.worker = VideoCaptureWorker(camera_index=0)
        self.thread = VideoThread(self.worker)

        # Smoothing for predictions
        self._stable_label: Optional[str] = None
        self._stable_count: int = 0
        self._last_append_ts: float = 0.0
        self._min_consistency: int = 3
        self._min_confidence: float = 0.55
        self._append_cooldown_s: float = 0.7

        # Left: camera and ROI
        self.camera_label = ImageLabel()
        self.roi_label = ImageLabel()
        self.roi_label.setMinimumSize(QSize(224, 224))

        # Text area: predicted sentence
        self.sentence_box = QTextEdit()
        self.sentence_box.setReadOnly(False)
        self.sentence_box.setPlaceholderText("Predicted text will appear here…")
        self.sentence_box.setFixedHeight(120)

        # Controls
        self.btn_clear = QPushButton("Clear All")
        self.btn_space = QPushButton("Space")
        self.btn_backspace = QPushButton("Delete")
        self.btn_save_txt = QPushButton("Save to a Text File")
        for b in (self.btn_clear, self.btn_space, self.btn_backspace, self.btn_save_txt):
            b.setFixedHeight(40)

        self.btn_clear.clicked.connect(lambda: self.sentence_box.clear())
        self.btn_space.clicked.connect(lambda: self.sentence_box.insertPlainText(" "))
        self.btn_backspace.clicked.connect(self._delete_last)
        self.btn_save_txt.clicked.connect(self._save_text)

        # Alphabet grid with images (optional placeholders)
        grid = QGridLayout()
        letters = [
            "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
        ]
        self.letter_labels = []
        for idx, ch in enumerate(letters):
            lbl = QLabel(ch)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setMinimumSize(QSize(64, 64))
            lbl.setStyleSheet("background:#222; color:#ddd; border:1px solid #333; border-radius:4px;")
            grid.addWidget(lbl, idx // 9, idx % 9)
            self.letter_labels.append(lbl)
        gridbox = QGroupBox("Alphabet")
        gridbox.setLayout(grid)

        # Top toolbar
        toolbar = QToolBar("Main")
        toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(toolbar)

        act_load_plugin = QAction(QIcon(), "Load Model Plugin", self)
        act_start = QAction(QIcon(), "Start Camera", self)
        act_stop = QAction(QIcon(), "Stop", self)
        act_set_roi = QAction(QIcon(), "Set ROI", self)
        toolbar.addAction(act_load_plugin)
        toolbar.addSeparator()
        toolbar.addAction(act_start)
        toolbar.addAction(act_stop)
        toolbar.addSeparator()
        toolbar.addAction(act_set_roi)

        act_load_plugin.triggered.connect(self._choose_plugin)
        act_start.triggered.connect(self._start_camera)
        act_stop.triggered.connect(self._stop_camera)
        act_set_roi.triggered.connect(self._prompt_roi)

        # Layouts
        left_col = QVBoxLayout()
        left_col.addWidget(self.camera_label)
        left_col.addWidget(self.sentence_box)

        button_row = QHBoxLayout()
        button_row.addWidget(self.btn_clear)
        button_row.addWidget(self.btn_space)
        button_row.addWidget(self.btn_backspace)
        button_row.addWidget(self.btn_save_txt)
        left_col.addLayout(button_row)

        right_col = QVBoxLayout()
        right_col.addWidget(self.roi_label)
        right_col.addWidget(gridbox)

        root = QHBoxLayout()
        left_widget = QWidget()
        left_widget.setLayout(left_col)
        right_widget = QWidget()
        right_widget.setLayout(right_col)
        root.addWidget(left_widget, 2)
        root.addWidget(right_widget, 1)

        container = QWidget()
        container.setLayout(root)
        self.setCentralWidget(container)

        # Wire signals
        self.worker.frame_ready.connect(self.camera_label.update_image)
        self.worker.roi_frame_ready.connect(self.roi_label.update_image)
        self.worker.prediction_ready.connect(self._on_prediction)
        self.worker.error.connect(self._on_error)

        # Status bar
        self.statusBar().showMessage("Ready")

    def closeEvent(self, event):  # noqa: N802
        self._stop_camera()
        event.accept()

    def _on_prediction(self, pred: Prediction):
        # Update live status
        self.statusBar().showMessage(f"Prediction: {pred.label} ({pred.confidence:.2f})")
        if not pred.label:
            return

        key = pred.label
        now = pred.timestamp_s if pred.timestamp_s else 0.0

        # Normalize some control labels
        is_space = key.lower() in {"space", "_"}
        is_delete = key.lower() in {"del", "delete", "backspace"}

        if is_space or is_delete:
            # Act immediately on controls but observe a small cooldown to avoid repeats
            if now - self._last_append_ts < self._append_cooldown_s:
                return
            if is_space:
                self.sentence_box.insertPlainText(" ")
            else:
                self._delete_last()
            self._last_append_ts = now
            self._stable_label = None
            self._stable_count = 0
            return

        # Smoothing for A..Z letters
        if key == self._stable_label and pred.confidence >= self._min_confidence:
            self._stable_count += 1
        else:
            self._stable_label = key
            self._stable_count = 1 if pred.confidence >= self._min_confidence else 0

        if (
            self._stable_count >= self._min_consistency
            and now - self._last_append_ts >= self._append_cooldown_s
        ):
            self.sentence_box.insertPlainText(key)
            self._last_append_ts = now
            self._stable_count = 0

    def _on_error(self, msg: str):
        QMessageBox.critical(self, "Error", msg)

    def _delete_last(self):
        text = self.sentence_box.toPlainText()
        if text:
            self.sentence_box.setPlainText(text[:-1])
            cursor = self.sentence_box.textCursor()
            cursor.movePosition(cursor.End)
            self.sentence_box.setTextCursor(cursor)

    def _save_text(self):
        text = self.sentence_box.toPlainText()
        if not text:
            QMessageBox.information(self, "Save", "Nothing to save.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save Text", str(Path.home() / f"sign_{dt.datetime.now():%Y%m%d_%H%M%S}.txt"), "Text Files (*.txt)")
        if path:
            Path(path).write_text(text, encoding="utf-8")

    def _choose_plugin(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose Model Plugin (.py)", str(Path.cwd()), "Python Files (*.py)")
        if not path:
            return
        try:
            recognizer = load_plugin(path)
        except Exception as exc:  # noqa: BLE001
            self._on_error(f"Failed to load plugin: {exc}")
            return
        self.recognizer = recognizer
        self.worker.set_recognizer(recognizer)
        QMessageBox.information(self, "Model", "Model loaded successfully.")

    def _start_camera(self):
        if not self.thread.isRunning():
            self.thread.start()

    def _stop_camera(self):
        if self.thread.isRunning():
            self.worker.stop()
            self.thread.stop()

    def _prompt_roi(self):
        dlg = RoiDialog(self)
        if dlg.exec():
            x, y, w, h = dlg.get_values()
            self.worker.set_roi(Roi(x, y, w, h))


class RoiDialog(QMessageBox):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Set ROI (x,y,w,h)")
        self.inputs = [QLineEdit(self) for _ in range(4)]
        for i, placeholder in enumerate(["x", "y", "w", "h"]):
            self.inputs[i].setPlaceholderText(placeholder)
        layout = QGridLayout()
        for i, label in enumerate(["x", "y", "w", "h"]):
            layout.addWidget(QLabel(label), 0, i)
            layout.addWidget(self.inputs[i], 1, i)
        w = QWidget(self)
        w.setLayout(layout)
        self.setIcon(QMessageBox.Question)
        self.setText("Enter ROI coordinates in pixels.")
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.layout().addWidget(w, 1, 0, 1, self.layout().columnCount())

    def get_values(self):
        try:
            values = [int(inp.text()) for inp in self.inputs]
        except ValueError:
            values = [0, 0, 224, 224]
        return values
