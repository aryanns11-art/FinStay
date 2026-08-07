from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
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
from app.controllers.transaction_controller import TransactionController

from PySide6.QtWidgets import QMessageBox
from app.models.transaction import Transaction

class TransactionPage(QWidget):
    """Transactions page."""

    transactions_changed = Signal()

    def __init__(self,session):
        super().__init__()
        
        self.session = session
        self.transaction_controller = TransactionController(session)

        self.init_ui()
        self.load_transactions()

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

        self.search_edit.textChanged.connect(
            self.search_transactions
        )

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(
            [
                "All",
                "Income",
                "Expense",
            ]
        )
        self.filter_combo.currentTextChanged.connect(
            self.filter_transactions
        )

        self.add_button = QPushButton("+ Add Transaction")

        self.add_button.clicked.connect(
            self.open_transaction_dialog
        )

        self.delete_button = QPushButton("Delete")

        self.delete_button.clicked.connect(
            self.delete_transaction
        )

        toolbar_layout.addWidget(self.search_edit)

        toolbar_layout.addWidget(self.filter_combo)

        toolbar_layout.addStretch()

        toolbar_layout.addWidget(self.add_button)

        toolbar_layout.addWidget(self.delete_button)

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

        if dialog.exec():
            self.load_transactions()
            self.transactions_changed.emit()

    def load_transactions(self):
        """Load all transactions into the table."""

        transactions = self.transaction_controller.get_transactions()
        self.populate_table(transactions)


    def search_transactions(self, text):

        text = text.strip()

        if not text:
            self.load_transactions()
            return

        transactions = (
            self.transaction_controller.search_transactions(text)
        )

        self.populate_table(transactions)

        
    def delete_transaction(self):

        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a transaction first."
            )
            return


        transaction_id = self.table.item(
            row,
            0
        ).data(Qt.UserRole)


        transaction = (
            self.session.query(Transaction)
            .filter(Transaction.id == transaction_id)
            .first()
        )


        if transaction:

            confirm = QMessageBox.question(
                self,
                "Confirm Delete",
                "Delete this transaction?"
            )


            if confirm == QMessageBox.Yes:

                self.transaction_controller.delete_transaction(
                    transaction
                )

                self.load_transactions()
                self.transactions_changed.emit()

    def populate_table(self, transactions):

        self.table.clearContents()
        self.table.clearSpans()

        self.table.setRowCount(len(transactions))

        for row, transaction in enumerate(transactions):

            self.table.setRowHeight(row, 40)

            date_item = QTableWidgetItem(transaction.transaction_date.strftime("%d-%m-%Y"))
            date_item.setData(Qt.UserRole,transaction.id)

            self.table.setItem(row,0,date_item)
            self.table.setItem(row,1,QTableWidgetItem(transaction.transaction_time.strftime("%H:%M")))
            self.table.setItem(row,2,QTableWidgetItem(transaction.category.name))
            self.table.setItem(row,3,QTableWidgetItem(f"₹ {transaction.amount:.2f}"))
            self.table.setItem(row,4,QTableWidgetItem(transaction.payment_method.name))
            self.table.setItem(row,5,QTableWidgetItem(transaction.description or ""))

        if not transactions:
            self.table.setRowCount(1)
            self.table.clearSelection()
            self.table.setItem(
                0,
                0,
                QTableWidgetItem("No transactions found.")
            )
            self.table.setSpan(0, 0, 1, 6)

    def filter_transactions(self, transaction_type):
        """Filter transactions by type."""
    
        if transaction_type == "All":
            self.load_transactions()
            return
    
        transactions = (
            self.transaction_controller.get_transactions_by_type(
                transaction_type
            )
        )
    
        self.populate_table(transactions)
