from __future__ import annotations

from typing import Iterable, List

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QLabel, QScrollArea, QWidget


def _make_tile(letter: str) -> QWidget:
    w = QWidget()
    label = QLabel(letter)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setMinimumSize(90, 90)
    label.setStyleSheet(
        "background-color: #2b2b2b; color: #eee; border-radius: 8px; border: 1px solid #444;"
    )
    label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
    layout = QGridLayout(w)
    layout.addWidget(label, 0, 0)
    return w


class LettersPanel(QWidget):
    """Reference panel showing the alphabet and special tokens."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Sign Language Alphabet - Reference")
        self.setMinimumSize(600, 400)
        base = QWidget()
        grid = QGridLayout(base)
        grid.setSpacing(8)

        letters: List[str] = [chr(ord("A") + i) for i in range(26)] + ["Space", "Delete"]
        for idx, ch in enumerate(letters):
            r, c = divmod(idx, 6)
            grid.addWidget(_make_tile(ch), r, c)

        scroll = QScrollArea(self)
        scroll.setWidget(base)
        scroll.setWidgetResizable(True)
        layout = QGridLayout(self)
        layout.addWidget(scroll, 0, 0)
