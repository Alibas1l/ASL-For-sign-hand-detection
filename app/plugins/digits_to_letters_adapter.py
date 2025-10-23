from __future__ import annotations

"""
Adapter plugin to map digit-classifier outputs to letters/controls.

Use this if your model predicts digits 0-9 (or 0-25) and you want to convert
sequences into letters or directly map classes to A..Z. Customize the mapping
by editing `class_to_label`.
"""

from typing import Sequence, List
import time
import numpy as np

from app.core.recognizer import BaseRecognizer, Prediction


class DigitsToLettersAdapter:
    labels: Sequence[str] = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["space", "delete"]

    def __init__(self, underlying_model=None):
        # Replace with your actual model bridge e.g., self.model = MyDigitModel()
        self.model = underlying_model
        self.class_to_label: List[str] = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def load(self) -> None:
        if self.model is not None and hasattr(self.model, "load"):
            self.model.load()

    def predict(self, image_bgr: np.ndarray) -> Prediction:
        # If you have an underlying digit model, get class index here.
        # Below is a placeholder: pick a pseudo class based on mean intensity.
        # Replace with: idx = self.model.predict(image_bgr)
        m = int(np.clip(image_bgr.mean(), 0, 255))
        idx = (m * len(self.class_to_label)) // 256
        idx = int(max(0, min(idx, len(self.class_to_label) - 1)))
        label = self.class_to_label[idx]
        return Prediction(label=label, confidence=0.9, timestamp_s=time.time())

    def get_labels(self) -> Sequence[str]:
        return self.labels
