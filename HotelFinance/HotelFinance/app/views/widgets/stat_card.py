from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class StatCard(QFrame):
    """Reusable dashboard statistics card."""

    def __init__(self, title: str, value: str):
        super().__init__()

        self.setObjectName("statCard")

        self.setFixedHeight(110)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("cardTitle")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("cardValue")
        self.value_label.setAlignment(Qt.AlignLeft)

        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.value_label)

    def set_value(self, value: str):
        """Update card value."""
        self.value_label.setText(value)