from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from app.views.dialogs.transaction_dialog import TransactionDialog


class TransactionPage(QWidget):
    """Transactions page."""

    def __init__(self,session):
        super().__init__()

        self.session = session

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # =====================================================
        # Header
        # =====================================================

        header_layout = QHBoxLayout()

        title = QLabel("Transactions")
        title.setObjectName("pageTitle")

        date_label = QLabel(
            datetime.now().strftime("%A, %d %b %Y")
        )
        date_label.setObjectName("dateLabel")

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(date_label)

        main_layout.addLayout(header_layout)

        # =====================================================
        # Toolbar
        # =====================================================

        toolbar_layout = QHBoxLayout()

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText(
            "Search transactions..."
        )

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(
            [
                "All",
                "Income",
                "Expense",
            ]
        )

        self.add_button = QPushButton("+ Add Transaction")

        self.add_button.clicked.connect(
            self.open_transaction_dialog
        )

        toolbar_layout.addWidget(self.search_edit)

        toolbar_layout.addWidget(self.filter_combo)

        toolbar_layout.addStretch()

        toolbar_layout.addWidget(self.add_button)

        main_layout.addLayout(toolbar_layout)

        # =====================================================
        # Transactions Table
        # =====================================================

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels(
            [
                "Date",
                "Time",
                "Category",
                "Amount",
                "Payment",
                "Description",
            ]
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.verticalHeader().setVisible(False)

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setAlternatingRowColors(True)

        self.table.setRowCount(1)

        self.table.setItem(
            0,
            0,
            QTableWidgetItem("No transactions found.")
        )

        self.table.setSpan(0, 0, 1, 6)

        main_layout.addWidget(self.table)

    # =========================================================
    # Dialog
    # =========================================================

    def open_transaction_dialog(self):
        dialog = TransactionDialog(self.session)

        dialog.exec()