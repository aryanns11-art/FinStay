from PySide6.QtWidgets import QStatusBar


class StatusBar(QStatusBar):
    """Application status bar."""

    def __init__(self):
        super().__init__()
