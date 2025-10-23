from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence
import numpy as np


@dataclass(frozen=True)
class Prediction:
    label: str
    confidence: float
    timestamp_s: float


class BaseRecognizer(Protocol):
    """Protocol for pluggable sign recognizers.

    Implementations should be deterministic and thread-safe for repeated calls to
    `predict` from a single thread. Heavy models should lazily initialize any
    runtimes in `load`.
    """

    labels: Sequence[str]

    def load(self) -> None:
        """Load model weights and resources."""

    def predict(self, image_bgr: np.ndarray) -> Prediction:
        """Return the top-1 prediction for the provided BGR image.

        Implementations should accept arbitrary HxWx3 uint8 arrays in BGR order.
        """

    def get_labels(self) -> Sequence[str]:
        return self.labels
