from __future__ import annotations

from typing import Tuple

import numpy as np
from PySide6.QtGui import QImage


def convert_bgr_to_qimage(frame_bgr: np.ndarray) -> QImage:
    """Convert an OpenCV BGR frame (H, W, 3) into a QImage.

    The resulting QImage uses RGB888 format and shares memory with a copied
    numpy array to ensure the data remains valid for painting.
    """
    if frame_bgr is None or frame_bgr.size == 0:
        raise ValueError("Empty frame passed to convert_bgr_to_qimage")

    if frame_bgr.ndim != 3 or frame_bgr.shape[2] != 3:
        raise ValueError("Expected BGR frame with shape (H, W, 3)")

    # Convert BGR -> RGB
    frame_rgb = frame_bgr[:, :, ::-1].copy(order="C")
    height, width = frame_rgb.shape[:2]
    bytes_per_line = 3 * width
    return QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888).copy()


def crop_roi(frame_bgr: np.ndarray, roi_norm: Tuple[float, float, float, float]) -> np.ndarray:
    """Crop a region of interest from a frame using normalized coords.

    roi_norm = (x, y, w, h) with each value in [0, 1] relative to frame size.
    Values are clamped to image bounds.
    """
    h, w = frame_bgr.shape[:2]
    x, y, rw, rh = roi_norm
    x = max(0.0, min(1.0, x))
    y = max(0.0, min(1.0, y))
    rw = max(0.0, min(1.0 - x, rw))
    rh = max(0.0, min(1.0 - y, rh))

    x0 = int(round(x * w))
    y0 = int(round(y * h))
    x1 = int(round((x + rw) * w))
    y1 = int(round((y + rh) * h))
    x1 = max(x0 + 1, min(w, x1))
    y1 = max(y0 + 1, min(h, y1))

    return frame_bgr[y0:y1, x0:x1]
