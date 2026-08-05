import qtawesome as qta

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton


class NavigationButton(QPushButton):
    """Sidebar navigation button."""

    def __init__(self, text: str, icon: str):
        super().__init__(text)

        self.setIcon(qta.icon(icon, color="white"))
        self.setIconSize(QSize(18, 18))

        self.setMinimumHeight(48)
        self.setCheckable(True)

        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
                text-align: left;
                font-size: 14px;
            }

            QPushButton:hover {
                background: #2D2D2D;
            }

            QPushButton:checked {
                background: #3B82F6;
            }
        """)