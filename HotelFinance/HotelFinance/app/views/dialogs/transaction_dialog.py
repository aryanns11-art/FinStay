from PySide6.QtCore import QDate, QTime

from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QTimeEdit,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
)
from app.views.dialogs.base_dialog import BaseDialog
from app.controllers.category_controller import CategoryController

from app.controllers.category_controller import CategoryController
from app.controllers.payment_method_controller import (
    PaymentMethodController,
)


class TransactionDialog(BaseDialog):
    """Dialog for adding a transaction."""

    def __init__(self,session   ):
        super().__init__("Add Transaction")

        self.session = session

        self.category_controller = CategoryController(session)

        self.payment_method_controller = PaymentMethodController(session)

        self.build_ui()

        self.load_categories()

        self.load_payment_methods()

    def load_categories(self):
        """Load categories into the combo box."""

        self.category_combo.clear()

        categories = self.category_controller.get_categories()

        for category in categories:
            self.category_combo.addItem(
                category.name,
                category.id,
            )

    def load_payment_methods(self):
        """Load payment methods into the combo box."""

        self.payment_method_combo.clear()

        methods = self.payment_method_controller.get_payment_methods()

        for method in methods:
            self.payment_method_combo.addItem(
                method.name,
                method.id,
            )

    def test_data(self):
        print("Category ID:", self.category_combo.currentData())
        print("Payment Method ID:", self.payment_method_combo.currentData())
        print("Amount:", self.amount_spin.value())
        print("Description:", self.description_edit.text())
        print("Date:", self.date_edit.date().toPython())
        print("Time:", self.time_edit.time().toPython())

        self.accept()

    def build_ui(self):

        form = QFormLayout()
        form.setSpacing(15)

        # Category
        self.category_combo = QComboBox()

        # Payment Method
        self.payment_method_combo = QComboBox()

        # Amount
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setPrefix("₹ ")
        self.amount_spin.setDecimals(2)
        self.amount_spin.setMaximum(999999999)

        # Description
        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText(
            "Optional description..."
        )

        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        # Time
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

        self.button_box.accepted.connect(self.test_data)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)