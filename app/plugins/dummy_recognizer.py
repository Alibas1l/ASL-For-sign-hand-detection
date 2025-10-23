from __future__ import annotations

import random
import time
from typing import Sequence

import cv2
import numpy as np

from app.core.recognizer import BaseRecognizer, Prediction


class DummyRecognizer:
    labels: Sequence[str] = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["space", "delete"]

    def __init__(self):
        self._rng = random.Random(42)

    def load(self) -> None:  # noqa: D401
        """No-op load for dummy recognizer."""
        return None

    def predict(self, image_bgr: np.ndarray) -> Prediction:
        # Very naive heuristic: threshold mean brightness to pick deterministic label bucket
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        m = int(np.clip(gray.mean(), 0, 255))
        idx = (m * len(self.labels)) // 256
        idx = min(idx, len(self.labels) - 1)
        label = self.labels[idx]
        conf = 0.5 + (m % 50) / 100.0
        return Prediction(label=label, confidence=float(conf), timestamp_s=time.time())

    def get_labels(self):
        return self.labels
