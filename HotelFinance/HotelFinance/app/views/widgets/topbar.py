from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget


class TopBar(QWidget):
    """Top navigation bar."""

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        title = QLabel("Hotel Expense Tracker")

        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layout.addWidget(title)
        layout.addStretch()