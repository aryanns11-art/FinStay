from PySide6.QtCore import QDate, QTime

from PySide6.QtWidgets import ( QComboBox, QDateEdit, QTimeEdit, QDialogButtonBox, QDoubleSpinBox, QFormLayout, QLineEdit, QMessageBox,)
from sqlalchemy.exc import SQLAlchemyError
from app.views.dialogs.base_dialog import BaseDialog
from app.controllers.category_controller import CategoryController

from app.controllers.payment_method_controller import (PaymentMethodController,)

from app.controllers.transaction_controller import TransactionController
from app.models.transaction import Transaction

class TransactionDialog(BaseDialog):
    """Dialog for adding a transaction."""

    def __init__(self,session   ):
        super().__init__("Add Transaction")

        self.session = session

        self.category_controller = CategoryController(session)
        self.payment_method_controller = PaymentMethodController(session)
        self.transaction_controller = TransactionController(session)

        self.build_ui()
        self.load_categories()
        self.load_payment_methods()

    def load_categories(self):
        """Load categories into the combo box."""

        self.category_combo.clear()

        try:
            categories = self.category_controller.get_categories()
        except SQLAlchemyError:
            QMessageBox.critical(
                self,
                "Database Error",
                "Unable to load transaction categories. Please check the database connection and try again.",
            )
            return

        for category in categories:
            self.category_combo.addItem(category.name,category.id,)

    def load_payment_methods(self):
        """Load payment methods into the combo box."""

        self.payment_method_combo.clear()

        try:
            methods = self.payment_method_controller.get_payment_methods()
        except SQLAlchemyError:
            QMessageBox.critical(
                self,
                "Database Error",
                "Unable to load payment methods. Please check the database connection and try again.",
            )
            return

        for method in methods:
            self.payment_method_combo.addItem(method.name,method.id,)

    def save_transaction(self):
        """Save a transaction to the database."""
    
        transaction = Transaction(
            category_id=self.category_combo.currentData(),
            payment_method_id=self.payment_method_combo.currentData(),
            amount=self.amount_spin.value(),
            description=self.description_edit.text().strip() or None,
            transaction_date=self.date_edit.date().toPython(),
            transaction_time=self.time_edit.time().toPython(),
        )
    
        try:
            self.transaction_controller.add_transaction(transaction)
            self.accept()
    
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Transaction",
                "Please enter a valid amount greater than zero.",
            )
        except SQLAlchemyError:
            QMessageBox.critical(
                self,
                "Unable to Save Transaction",
                "The transaction could not be saved. Please try again.",
            )

    def build_ui(self):

        form = QFormLayout()
        form.setSpacing(15)

        self.category_combo = QComboBox()

        self.payment_method_combo = QComboBox()

        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setPrefix("₹ ")
        self.amount_spin.setDecimals(2)
        self.amount_spin.setMaximum(999999999)

        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("Optional description...")

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())

        form.addRow("Category *", self.category_combo)
        form.addRow("Payment Method *", self.payment_method_combo)
        form.addRow("Amount *", self.amount_spin)
        form.addRow("Description", self.description_edit)
        form.addRow("Transaction Date", self.date_edit)
        form.addRow("Transaction Time", self.time_edit)

        self.layout.addLayout(form)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )

        self.button_box.accepted.connect(self.save_transaction)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
