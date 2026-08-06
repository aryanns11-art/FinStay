from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
)


class BaseDialog(QDialog):
    """Base class for all dialogs."""

    def __init__(self, title: str):
        super().__init__()

        self.setWindowTitle(title)

        self.setModal(True)

        self.resize(800, 600)

        self.setMinimumSize(700, 550)

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(25, 25, 25, 25)

        self.layout.setSpacing(20)

        title_label = QLabel(title)

        title_label.setObjectName("dialogTitle")

        title_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(title_label)