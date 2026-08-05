from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QDateEdit,
    QTimeEdit,
    QPushButton,
    QFrame,
)


class TransactionPage(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout(self)

        # ================= Header =================

        header = QLabel("Transactions")
        header.setObjectName("pageTitle")

        main_layout.addWidget(header)

        # ================= Form Card =================

        form_card = QFrame()
        form_card.setObjectName("statCard")

        form_layout = QFormLayout(form_card)

        form_layout.setSpacing(15)

        # Category

        self.category_combo = QComboBox()

        self.category_combo.addItems([
            "Business",
            "Employee Salary",
            "Personal",
            "Education",
            "Maintenance",
            "Electricity",
            "Water",
            "Food",
            "Fuel",
            "Other",
        ])

        # Type

        self.type_combo = QComboBox()

        self.type_combo.addItems([
            "Income",
            "Expense",
        ])

        # Amount

        self.amount_spin = QDoubleSpinBox()

        self.amount_spin.setMaximum(100000000)

        self.amount_spin.setPrefix("₹ ")

        self.amount_spin.setDecimals(2)

        # Payment Method

        self.payment_combo = QComboBox()

        self.payment_combo.addItems([
            "Cash",
            "UPI",
            "Bank Transfer",
            "Card",
        ])

        # Description

        self.description_edit = QLineEdit()

        # Date

        self.date_edit = QDateEdit()

        self.date_edit.setCalendarPopup(True)

        self.date_edit.setDate(QDate.currentDate())

        # Time

        self.time_edit = QTimeEdit()

        self.time_edit.setTime(QTime.currentTime())

        # Save Button

        self.save_button = QPushButton("Save Transaction")

        form_layout.addRow("Category", self.category_combo)
        form_layout.addRow("Type", self.type_combo)
        form_layout.addRow("Amount", self.amount_spin)
        form_layout.addRow("Payment Method", self.payment_combo)
        form_layout.addRow("Description", self.description_edit)
        form_layout.addRow("Date", self.date_edit)
        form_layout.addRow("Time", self.time_edit)
        form_layout.addRow("", self.save_button)

        main_layout.addWidget(form_card)

        main_layout.addStretch()