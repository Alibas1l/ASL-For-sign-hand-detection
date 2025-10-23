from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QImage, QMouseEvent, QPainter, QPen
from PySide6.QtWidgets import QLabel


@dataclass
class _DragState:
    dragging: bool = False
    resizing: bool = False
    drag_origin: Optional[QPointF] = None
    roi_origin: Optional[QRectF] = None
    edge: Optional[str] = None  # 'left', 'right', 'top', 'bottom', 'topleft', ...


class VideoWidget(QLabel):
    """Widget that displays frames and an adjustable ROI overlay."""

    roiChanged = Signal(tuple)  # (x, y, w, h) normalized

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._image: Optional[QImage] = None
        self._roi_norm: Tuple[float, float, float, float] = (0.55, 0.15, 0.4, 0.7)
        self._drag = _DragState()
        self.setMinimumSize(640, 360)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: #111;")

    # Public API -----------------------------------------------------------

    def set_frame(self, image: QImage) -> None:
        self._image = image
        self.update()

    def set_roi_norm(self, roi: Tuple[float, float, float, float]) -> None:
        self._roi_norm = roi
        self.update()

    def get_roi_norm(self) -> Tuple[float, float, float, float]:
        return self._roi_norm

    # Painting -------------------------------------------------------------

    def paintEvent(self, event):  # noqa: N802 - Qt API
        super().paintEvent(event)
        if self._image is None:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        # Draw the image scaled to fit while preserving aspect ratio
        pixmap = self._image
        # Calculate target rect
        target_rect = QRectF(self.rect())
        img_rect = QRectF(0, 0, pixmap.width(), pixmap.height())
        scaled = img_rect
        scaled = self._fit_rect(img_rect, target_rect)
        painter.drawImage(scaled, pixmap)

        # ROI overlay in widget coords based on scaled area
        roi_rect = self._roi_rect_in_widget(scaled)
        pen = QPen(QColor(255, 170, 0), 3)
        painter.setPen(pen)
        painter.drawRect(roi_rect)
        painter.fillRect(roi_rect.adjusted(0, 0, 0, 0), QColor(255, 170, 0, 40))
        painter.end()

    # Mouse interaction ----------------------------------------------------

    def mousePressEvent(self, event: QMouseEvent):  # noqa: N802 - Qt API
        if self._image is None:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            roi_rect = self._roi_rect_in_widget(self._fit_rect(QRectF(0, 0, self._image.width(), self._image.height()), QRectF(self.rect())))
            margin = 10
            pos = QPointF(event.position())
            if roi_rect.contains(pos):
                edge = self._hit_test_edge(roi_rect, pos, margin)
                self._drag = _DragState(dragging=True, resizing=edge is not None, drag_origin=pos, roi_origin=roi_rect, edge=edge)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):  # noqa: N802 - Qt API
        if not self._drag.dragging or self._image is None:
            return
        pos = QPointF(event.position())
        widget_img_rect = self._fit_rect(QRectF(0, 0, self._image.width(), self._image.height()), QRectF(self.rect()))
        roi_rect = QRectF(self._drag.roi_origin)
        delta = pos - self._drag.drag_origin
        if self._drag.resizing and self._drag.edge:
            if "left" in self._drag.edge:
                roi_rect.setLeft(max(widget_img_rect.left(), min(roi_rect.right() - 20, roi_rect.left() + delta.x())))
            if "right" in self._drag.edge:
                roi_rect.setRight(min(widget_img_rect.right(), max(roi_rect.left() + 20, roi_rect.right() + delta.x())))
            if "top" in self._drag.edge:
                roi_rect.setTop(max(widget_img_rect.top(), min(roi_rect.bottom() - 20, roi_rect.top() + delta.y())))
            if "bottom" in self._drag.edge:
                roi_rect.setBottom(min(widget_img_rect.bottom(), max(roi_rect.top() + 20, roi_rect.bottom() + delta.y())))
        else:
            # Move
            roi_rect.translate(delta)
            if roi_rect.left() < widget_img_rect.left():
                roi_rect.moveLeft(widget_img_rect.left())
            if roi_rect.top() < widget_img_rect.top():
                roi_rect.moveTop(widget_img_rect.top())
            if roi_rect.right() > widget_img_rect.right():
                roi_rect.moveRight(widget_img_rect.right())
            if roi_rect.bottom() > widget_img_rect.bottom():
                roi_rect.moveBottom(widget_img_rect.bottom())
        # Convert back to normalized coords based on image size and scaled rect
        self._roi_norm = self._roi_norm_from_widget(widget_img_rect, roi_rect)
        self._drag.roi_origin = roi_rect
        self._drag.drag_origin = pos
        self.roiChanged.emit(self._roi_norm)
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):  # noqa: N802 - Qt API
        self._drag = _DragState()
        super().mouseReleaseEvent(event)

    # Helpers --------------------------------------------------------------

    def _hit_test_edge(self, rect: QRectF, pos: QPointF, margin: float) -> Optional[str]:
        left = abs(pos.x() - rect.left()) <= margin
        right = abs(pos.x() - rect.right()) <= margin
        top = abs(pos.y() - rect.top()) <= margin
        bottom = abs(pos.y() - rect.bottom()) <= margin
        if left and top:
            return "topleft"
        if right and top:
            return "topright"
        if left and bottom:
            return "bottomleft"
        if right and bottom:
            return "bottomright"
        if left:
            return "left"
        if right:
            return "right"
        if top:
            return "top"
        if bottom:
            return "bottom"
        return None

    def _fit_rect(self, img_rect: QRectF, target_rect: QRectF) -> QRectF:
        # Preserve aspect ratio fit
        img_ratio = img_rect.width() / img_rect.height()
        target_ratio = target_rect.width() / target_rect.height() if target_rect.height() > 0 else img_ratio
        if img_ratio > target_ratio:
            # Width bound
            width = target_rect.width()
            height = width / img_ratio
            x = target_rect.left()
            y = target_rect.top() + (target_rect.height() - height) / 2
        else:
            height = target_rect.height()
            width = height * img_ratio
            y = target_rect.top()
            x = target_rect.left() + (target_rect.width() - width) / 2
        return QRectF(x, y, width, height)

    def _roi_rect_in_widget(self, scaled_img_rect: QRectF) -> QRectF:
        x, y, w, h = self._roi_norm
        rx = scaled_img_rect.left() + x * scaled_img_rect.width()
        ry = scaled_img_rect.top() + y * scaled_img_rect.height()
        rw = w * scaled_img_rect.width()
        rh = h * scaled_img_rect.height()
        return QRectF(rx, ry, rw, rh)

    def _roi_norm_from_widget(self, scaled_img_rect: QRectF, roi_in_widget: QRectF):
        x = (roi_in_widget.left() - scaled_img_rect.left()) / max(1.0, scaled_img_rect.width())
        y = (roi_in_widget.top() - scaled_img_rect.top()) / max(1.0, scaled_img_rect.height())
        w = roi_in_widget.width() / max(1.0, scaled_img_rect.width())
        h = roi_in_widget.height() / max(1.0, scaled_img_rect.height())
        x = min(max(0.0, x), 1.0)
        y = min(max(0.0, y), 1.0)
        w = min(max(0.02, w), 1.0 - x)
        h = min(max(0.02, h), 1.0 - y)
        return (x, y, w, h)
