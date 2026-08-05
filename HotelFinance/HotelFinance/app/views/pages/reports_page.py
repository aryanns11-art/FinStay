from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ReportsPage(QWidget):
    """Reports page."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Reports")
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)