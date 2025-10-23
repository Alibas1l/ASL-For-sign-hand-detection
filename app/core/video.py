from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional, Tuple

import cv2
import numpy as np
from PySide6.QtCore import QObject, Signal, QThread

from .recognizer import Prediction, BaseRecognizer


@dataclass
class Roi:
    x: int
    y: int
    w: int
    h: int

    def as_tuple(self) -> Tuple[int, int, int, int]:
        return self.x, self.y, self.w, self.h


class VideoCaptureWorker(QObject):
    frame_ready = Signal(np.ndarray)  # BGR frame
    roi_frame_ready = Signal(np.ndarray)  # BGR cropped roi
    prediction_ready = Signal(Prediction)
    error = Signal(str)

    def __init__(self, camera_index: int, recognizer: Optional[BaseRecognizer] = None):
        super().__init__()
        self._camera_index = camera_index
        self._recognizer = recognizer
        self._running = False
        self._roi: Optional[Roi] = None
        self._fps: float = 30.0

    def set_recognizer(self, recognizer: Optional[BaseRecognizer]):
        self._recognizer = recognizer

    def set_roi(self, roi: Optional[Roi]):
        self._roi = roi

    def start(self):
        self._running = True
        self._run()

    def stop(self):
        self._running = False

    def _run(self):
        cap = cv2.VideoCapture(self._camera_index)
        if not cap.isOpened():
            self.error.emit("Could not open camera")
            return
        cap.set(cv2.CAP_PROP_FPS, self._fps)
        try:
            last_pred_time = 0.0
            pred_interval = 1.0 / 5.0  # 5 Hz prediction
            while self._running:
                ok, frame = cap.read()
                if not ok:
                    self.error.emit("Failed to read frame")
                    break
                # Mirror for user-friendly view
                frame = cv2.flip(frame, 1)

                # Draw ROI if set
                roi_frame = None
                if self._roi is not None:
                    x, y, w, h = self._roi.as_tuple()
                    h_img, w_img = frame.shape[:2]
                    x = max(0, min(x, w_img - 1))
                    y = max(0, min(y, h_img - 1))
                    w = max(1, min(w, w_img - x))
                    h = max(1, min(h, h_img - y))
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 185, 255), 2)
                    roi_frame = frame[y : y + h, x : x + w]

                self.frame_ready.emit(frame)
                if roi_frame is not None:
                    self.roi_frame_ready.emit(roi_frame)

                # Periodic prediction
                now = time.time()
                if (
                    self._recognizer is not None
                    and roi_frame is not None
                    and now - last_pred_time >= pred_interval
                ):
                    try:
                        pred = self._recognizer.predict(roi_frame)
                        self.prediction_ready.emit(pred)
                    except Exception as exc:  # noqa: BLE001
                        self.error.emit(f"Prediction error: {exc}")
                    last_pred_time = now

                # Simple frame pacing
                if self._fps > 0:
                    time.sleep(max(0.0, (1.0 / self._fps) - 0.001))
        finally:
            cap.release()


class VideoThread(QThread):
    def __init__(self, worker: VideoCaptureWorker):
        super().__init__()
        self.worker = worker
        self.worker.moveToThread(self)

    def run(self):
        self.worker.start()

    def stop(self):
        self.worker.stop()
        self.quit()
        self.wait(1000)
