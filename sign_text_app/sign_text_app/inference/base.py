from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


@dataclass
class Prediction:
    label: str
    confidence: float


class ModelAdapter(ABC):
    """Abstract interface your model should implement.

    Implement `predict` to return a (label, confidence) for a given BGR ROI.
    """

    labels: List[str] = [
        *[chr(ord('A') + i) for i in range(26)],
        "space",
        "delete",
        "nothing",
    ]

    @abstractmethod
    def predict(self, roi_bgr: np.ndarray) -> Prediction:
        """Return a prediction for the provided ROI frame in BGR format."""
        raise NotImplementedError

    def warmup(self) -> None:
        """Optional: run a few dry passes to load kernels/weights."""
        return
