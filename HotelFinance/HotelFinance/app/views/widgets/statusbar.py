from PySide6.QtWidgets import QLabel, QStatusBar


class StatusBar(QStatusBar):
    """Application status bar."""

    def __init__(self):
        super().__init__()

        self.showMessage("Ready")

        self.addPermanentWidget(QLabel("PostgreSQL"))