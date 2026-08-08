from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget


class TopBar(QWidget):
    """Top navigation bar."""

    def __init__(self, hotel_name="Hotel Expense Tracker"):
        super().__init__()

        layout = QHBoxLayout(self)

        self.title_label = QLabel(hotel_name)

        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layout.addWidget(self.title_label)
        layout.addStretch()

    def set_hotel_name(self, hotel_name):
        self.title_label.setText(hotel_name)
