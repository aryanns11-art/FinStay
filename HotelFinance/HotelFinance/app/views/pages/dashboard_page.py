from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DashboardPage(QWidget):
    """Dashboard page."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Dashboard")
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)