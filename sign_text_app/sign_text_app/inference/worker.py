from __future__ import annotations

import time
from typing import Optional, Tuple

import cv2
import numpy as np
from PySide6.QtCore import QObject, QThread, QTimer, Signal

from ..utils.cv import crop_roi
from ..utils.smoothing import MajoritySmoother
from .base import ModelAdapter, Prediction


class CameraInferenceWorker(QObject):
    """Capture frames from webcam and run model inference on ROI.

    Emits:
      - frameReady(np.ndarray): latest full BGR frame
      - roiPrediction(Prediction): latest model prediction
      - fpsUpdated(float): rolling FPS
    """

    frameReady = Signal(np.ndarray)
    roiPrediction = Signal(object)  # Prediction
    fpsUpdated = Signal(float)

    def __init__(
        self,
        device_index: int,
        adapter: ModelAdapter,
        roi_norm: Tuple[float, float, float, float] = (0.55, 0.15, 0.4, 0.7),
        target_fps: int = 30,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._device_index = device_index
        self._adapter = adapter
        self._roi_norm = roi_norm
        self._target_interval_ms = max(1, int(1000 / max(1, target_fps)))

        self._thread: Optional[QThread] = None
        self._timer: Optional[QTimer] = None
        self._cap: Optional[cv2.VideoCapture] = None
        self._last_fps_ts: float = time.time()
        self._frame_counter: int = 0

    # Thread lifecycle -----------------------------------------------------

    def start(self) -> None:
        if self._thread is not None:
            return
        self._thread = QThread()
        self.moveToThread(self._thread)
        self._thread.started.connect(self._on_thread_started)
        self._thread.start()

    def stop(self) -> None:
        if self._thread is None:
            return
        if self._timer is not None:
            self._timer.stop()
            self._timer.deleteLater()
            self._timer = None
        if self._cap is not None:
            try:
                self._cap.release()
            except Exception:
                pass
            self._cap = None
        self._thread.quit()
        self._thread.wait(3000)
        self._thread = None

    # Public API -----------------------------------------------------------

    def set_roi_norm(self, roi_norm: Tuple[float, float, float, float]) -> None:
        self._roi_norm = roi_norm

    # Internal -------------------------------------------------------------

    def _on_thread_started(self) -> None:
        self._cap = cv2.VideoCapture(self._device_index)
        # Try to set a sane resolution for performance
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self._cap.set(cv2.CAP_PROP_FPS, 30)

        self._timer = QTimer()
        self._timer.setInterval(self._target_interval_ms)
        self._timer.timeout.connect(self._on_tick)
        self._timer.start()

    def _on_tick(self) -> None:
        if self._cap is None:
            return
        ret, frame = self._cap.read()
        if not ret or frame is None:
            return
        self.frameReady.emit(frame)

        roi = crop_roi(frame, self._roi_norm)
        try:
            pred = self._adapter.predict(roi)
        except Exception:
            # Do not crash the loop on model errors.
            pred = Prediction(label="nothing", confidence=0.0)
        self.roiPrediction.emit(pred)

        # FPS accounting
        self._frame_counter += 1
        now = time.time()
        if now - self._last_fps_ts >= 1.0:
            fps = self._frame_counter / (now - self._last_fps_ts)
            self._frame_counter = 0
            self._last_fps_ts = now
            self.fpsUpdated.emit(float(fps))
