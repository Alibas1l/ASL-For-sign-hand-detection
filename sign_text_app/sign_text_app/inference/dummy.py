from __future__ import annotations

import random
from typing import Optional

import numpy as np

from .base import ModelAdapter, Prediction


class NoOpAdapter(ModelAdapter):
    """Baseline adapter that returns 'nothing'. Useful for UI-only testing."""

    def predict(self, roi_bgr: np.ndarray) -> Prediction:
        return Prediction(label="nothing", confidence=0.0)


class RandomAdapter(ModelAdapter):
    """A naive adapter that randomly emits letters with moderate confidence.

    This is for demo only; replace with your trained model.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        self._rng = random.Random(seed)

    def predict(self, roi_bgr: np.ndarray) -> Prediction:
        # Bias towards 'nothing' to avoid spamming.
        if self._rng.random() < 0.7:
            return Prediction(label="nothing", confidence=0.3)
        label_pool = [chr(ord('A') + i) for i in range(26)] + ["space", "delete"]
        label = self._rng.choice(label_pool)
        conf = self._rng.uniform(0.6, 0.95)
        return Prediction(label=label, confidence=conf)
