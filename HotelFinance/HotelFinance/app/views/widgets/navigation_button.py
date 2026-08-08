import qtawesome as qta

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton


class NavigationButton(QPushButton):
    """Sidebar navigation button."""

    def __init__(self, text: str, icon: str):
        super().__init__(text)

        self.icon_name = icon
        self.setObjectName("navigationButton")
        self.setIconSize(QSize(18, 18))
        self.setMinimumHeight(48)
        self.setCheckable(True)
        self.toggled.connect(self.update_icon)
        self.update_icon(False)

    def update_icon(self, is_active):
        color = "#D4AF37" if is_active else "#D4D4D8"
        self.setIcon(qta.icon(self.icon_name, color=color))
