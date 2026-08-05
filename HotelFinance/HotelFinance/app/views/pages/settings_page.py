from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SettingsPage(QWidget):
    """Settings page."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Settings")
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)