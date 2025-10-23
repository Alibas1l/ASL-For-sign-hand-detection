from __future__ import annotations

from collections import deque, Counter
from dataclasses import dataclass
from typing import Deque, Optional, Tuple


@dataclass
class SmoothedPrediction:
    label: str
    confidence: float


class MajoritySmoother:
    """Temporal smoother that emits a stable label when confident enough.

    - Keeps a fixed-size window of (label, confidence)
    - When the most common label exceeds min_count and has avg_conf >= conf_th,
      it is considered stable and returned by `get_stable()`.
    """

    def __init__(self, window_size: int = 7, min_count: int = 4, conf_threshold: float = 0.6) -> None:
        self.window_size = window_size
        self.min_count = min_count
        self.conf_threshold = conf_threshold
        self._window: Deque[Tuple[str, float]] = deque(maxlen=window_size)

    def update(self, label: str, confidence: float) -> None:
        self._window.append((label, confidence))

    def get_stable(self) -> Optional[SmoothedPrediction]:
        if not self._window:
            return None
        labels = [l for l, _ in self._window]
        counts = Counter(labels)
        label, count = counts.most_common(1)[0]
        if count < self.min_count:
            return None
        avg_conf = sum(c for l, c in self._window if l == label) / count
        if avg_conf < self.conf_threshold:
            return None
        return SmoothedPrediction(label=label, confidence=avg_conf)
