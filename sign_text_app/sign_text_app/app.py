from __future__ import annotations

import argparse
import importlib
import os
from typing import Optional, Tuple, Type

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from .inference.base import ModelAdapter, Prediction
from .inference.dummy import NoOpAdapter
from .inference.worker import CameraInferenceWorker
from .utils.cv import convert_bgr_to_qimage
from .utils.smoothing import MajoritySmoother
from .widgets.letters_panel import LettersPanel
from .widgets.video_widget import VideoWidget


APP_STYLES = """
QMainWindow { background-color: #1a1a1a; }
QLabel, QPlainTextEdit { color: #e7e7e7; }
QPlainTextEdit { background-color: #0f0f0f; border: 1px solid #333; border-radius: 6px; }
QPushButton { background-color: #2a2a2a; color: #e7e7e7; border: 1px solid #444; border-radius: 6px; padding: 8px 12px; }
QPushButton:hover { background-color: #333; }
QPushButton:pressed { background-color: #222; }
QToolBar { background: #141414; border: none; }
"""


class MainWindow(QMainWindow):
    def __init__(self, adapter: ModelAdapter, device_index: int = 0) -> None:
        super().__init__()
        self.setWindowTitle("Sign Language to Text")
        self.resize(1080, 720)

        self._adapter = adapter
        self._smoother = MajoritySmoother(window_size=7, min_count=4, conf_threshold=0.65)

        # Central UI ------------------------------------------------------
        central = QWidget(self)
        vbox = QVBoxLayout(central)
        self.video = VideoWidget(self)
        vbox.addWidget(self.video, stretch=3)

        self.text_box = QPlainTextEdit(self)
        self.text_box.setPlaceholderText("Predicted text will appear here…")
        self.text_box.setMinimumHeight(120)
        vbox.addWidget(self.text_box, stretch=1)

        controls = QHBoxLayout()
        self.btn_clear = QPushButton("Clear All", self)
        self.btn_space = QPushButton("Space", self)
        self.btn_delete = QPushButton("Delete", self)
        self.btn_save = QPushButton("Save to a Text File", self)
        self.btn_quit = QPushButton("Quit", self)
        for b in (self.btn_clear, self.btn_space, self.btn_delete, self.btn_save, self.btn_quit):
            controls.addWidget(b)
        vbox.addLayout(controls)
        self.setCentralWidget(central)

        # Toolbar ---------------------------------------------------------
        tb = QToolBar("Main", self)
        self.addToolBar(tb)
        act_ref = QAction("Alphabet Reference", self)
        tb.addAction(act_ref)
        act_clear = QAction("Clear", self)
        tb.addAction(act_clear)
        act_save = QAction("Save", self)
        tb.addAction(act_save)
        act_quit = QAction("Quit", self)
        tb.addAction(act_quit)

        # Status bar ------------------------------------------------------
        sb = QStatusBar(self)
        self.setStatusBar(sb)
        self._status_pred = QLabel("–")
        self._status_fps = QLabel("FPS: –")
        sb.addPermanentWidget(self._status_pred)
        sb.addPermanentWidget(self._status_fps)

        # Secondary windows ----------------------------------------------
        self._letters_panel = LettersPanel(self)

        # Workers ---------------------------------------------------------
        self._worker = CameraInferenceWorker(device_index=device_index, adapter=adapter, roi_norm=self.video.get_roi_norm())
        self._worker.frameReady.connect(self._on_frame)
        self._worker.roiPrediction.connect(self._on_prediction)
        self._worker.fpsUpdated.connect(self._on_fps)
        self.video.roiChanged.connect(self._worker.set_roi_norm)
        self._worker.start()

        # Connections -----------------------------------------------------
        act_ref.triggered.connect(self._letters_panel.show)
        act_clear.triggered.connect(self._on_clear)
        act_save.triggered.connect(self._on_save)
        act_quit.triggered.connect(self.close)

        self.btn_clear.clicked.connect(self._on_clear)
        self.btn_space.clicked.connect(lambda: self._append_token("space"))
        self.btn_delete.clicked.connect(lambda: self._append_token("delete"))
        self.btn_save.clicked.connect(self._on_save)
        self.btn_quit.clicked.connect(self.close)

        self.setStyleSheet(APP_STYLES)

    # Event handlers ------------------------------------------------------

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802 - Qt API
        try:
            self._worker.stop()
        finally:
            event.accept()

    def _on_frame(self, frame_bgr: np.ndarray) -> None:
        image = convert_bgr_to_qimage(frame_bgr)
        self.video.set_frame(image)

    def _on_prediction(self, pred: Prediction) -> None:
        self._status_pred.setText(f"{pred.label} ({pred.confidence:.2f})")
        self._smoother.update(pred.label, pred.confidence)
        stable = self._smoother.get_stable()
        if stable is None:
            return
        self._append_token(stable.label)

    def _on_fps(self, fps: float) -> None:
        self._status_fps.setText(f"FPS: {fps:.1f}")

    def _append_token(self, token: str) -> None:
        if token == "nothing":
            return
        if token == "space":
            self.text_box.insertPlainText(" ")
            self.text_box.moveCursor(self.text_box.textCursor().End)
            return
        if token == "delete":
            cursor = self.text_box.textCursor()
            cursor.deletePreviousChar()
            return
        # Alphabet
        if len(token) == 1 and token.isalpha():
            self.text_box.insertPlainText(token)
            self.text_box.moveCursor(self.text_box.textCursor().End)

    def _on_clear(self) -> None:
        self.text_box.clear()

    def _on_save(self) -> None:
        text = self.text_box.toPlainText()
        if not text.strip():
            QMessageBox.information(self, "Nothing to save", "There is no text to save yet.")
            return
        file_name, _ = QFileDialog.getSaveFileName(self, "Save as", "sign_text.txt", "Text Files (*.txt)")
        if not file_name:
            return
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            QMessageBox.warning(self, "Save failed", f"Could not save file: {e}")


# Entrypoint ---------------------------------------------------------------


def _load_adapter(class_path: Optional[str]) -> ModelAdapter:
    if not class_path:
        return NoOpAdapter()
    module_name, _, class_name = class_path.rpartition(":")
    if not module_name:
        module_name, _, class_name = class_path.rpartition(".")
    if not module_name or not class_name:
        raise ValueError("--model-class must be 'module.sub:Class' or 'module.sub.Class'")
    module = importlib.import_module(module_name)
    adapter_cls = getattr(module, class_name)
    if not issubclass(adapter_cls, ModelAdapter):
        raise TypeError("Provided class is not a ModelAdapter")
    return adapter_cls()


def run(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Sign Language to Text App")
    parser.add_argument("--camera", type=int, default=0, help="Camera device index (default: 0)")
    parser.add_argument(
        "--model-class",
        type=str,
        default=os.environ.get("SIGN_APP_MODEL"),
        help="Dotted path to ModelAdapter class, e.g. 'my_pkg.adapter:MyAdapter'",
    )
    args = parser.parse_args(argv)

    app = QApplication([])
    win = MainWindow(adapter=_load_adapter(args.model_class), device_index=args.camera)
    win.show()
    app.exec()
