from datetime import datetime, date

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    QFrame,
)

from app.views.widgets.stat_card import StatCard

from app.controllers.transaction_controller import (TransactionController,)


class DashboardPage(QWidget):
    """Dashboard page."""

    def __init__(self, session):
        super().__init__()

        self.session = session

        self.transaction_controller = TransactionController(session)

        self.init_ui()

        self.load_dashboard()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(24)

        self.setStyleSheet(
            """
            QLabel#pageTitle {
                font-size: 24px;
                font-weight: 600;
                color: #F5F5F5;
            }

            QLabel#dateLabel {
                font-size: 11px;
                color: #9CA3AF;
            }

            QLabel#sectionTitle {
                font-size: 14px;
                font-weight: 600;
                color: #E5E7EB;
                margin-bottom: 2px;
            }

            QFrame#summaryCard {
                background-color: #1B1B1B;
                border: 1px solid #2A2A2A;
                border-radius: 16px;
            }

            QLabel#summaryCaption {
                font-size: 11px;
                color: #6B7280;
            }

            QLabel#summaryLabel {
                font-size: 12px;
                color: #A1A1AA;
            }

            QLabel#summaryValue {
                font-size: 15px;
                font-weight: 600;
                color: #F5F5F5;
            }
            """
        )

        # =====================================================
        # Header
        # =====================================================

        header_frame = QFrame()
        header_frame.setObjectName("dashboardHeader")

        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        date_label = QLabel(datetime.now().strftime("%A, %d %b %Y"))
        date_label.setObjectName("dateLabel")
        date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(date_label)

        main_layout.addWidget(header_frame)

        # =====================================================
        # Statistics Cards
        # =====================================================

        stats_layout = QGridLayout()
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(16)
        stats_layout.setColumnStretch(0, 1)
        stats_layout.setColumnStretch(1, 1)
        stats_layout.setColumnStretch(2, 1)
        stats_layout.setColumnStretch(3, 1)

        self.income_card = StatCard(
            "Today's Income",
            "₹0",
        )

        self.expense_card = StatCard(
            "Today's Expense",
            "₹0",
        )

        self.profit_card = StatCard(
            "Today's Net Profit",
            "₹0",
        )

        self.cash_income_card = StatCard(
            "Cash Income",
            "₹0",
        )

        self.cash_expense_card = StatCard(
            "Cash Expense",
            "₹0",
        )

        self.online_income_card = StatCard(
            "Online Income",
            "₹0",
        )

        self.online_expense_card = StatCard(
            "Online Expense",
            "₹0",
        )

        stats_layout.addWidget(self.profit_card, 0, 0)
        stats_layout.addWidget(self.income_card, 0, 1)
        stats_layout.addWidget(self.expense_card, 0, 2)
        stats_layout.addWidget(self.cash_income_card, 0, 3)

        stats_layout.addWidget(self.cash_expense_card, 1, 0)
        stats_layout.addWidget(self.online_income_card, 1, 1)
        stats_layout.addWidget(self.online_expense_card, 1, 2)

        main_layout.addLayout(stats_layout)

        # =====================================================
        # Today's Summary
        # =====================================================

        summary_title = QLabel("Today's Summary")
        summary_title.setObjectName("sectionTitle")

        main_layout.addWidget(summary_title)

        summary_frame = QFrame()
        summary_frame.setObjectName("summaryCard")

        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setContentsMargins(24, 24, 24, 24)
        summary_layout.setSpacing(16)

        summary_caption = QLabel("Key totals and leading entries")
        summary_caption.setObjectName("summaryCaption")
        summary_layout.addWidget(summary_caption)

        summary_grid = QGridLayout()
        summary_grid.setContentsMargins(0, 0, 0, 0)
        summary_grid.setHorizontalSpacing(18)
        summary_grid.setVerticalSpacing(12)

        self.income_count_label = QLabel("0")
        self.income_count_label.setObjectName("summaryValue")
        self.income_count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.expense_count_label = QLabel("0")
        self.expense_count_label.setObjectName("summaryValue")
        self.expense_count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.highest_income_label = QLabel("-")
        self.highest_income_label.setObjectName("summaryValue")
        self.highest_income_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.highest_income_amount = QLabel("₹0.00")
        self.highest_income_amount.setObjectName("summaryValue")
        self.highest_income_amount.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.highest_expense_label = QLabel("-")
        self.highest_expense_label.setObjectName("summaryValue")
        self.highest_expense_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.highest_expense_amount = QLabel("₹0.00")
        self.highest_expense_amount.setObjectName("summaryValue")
        self.highest_expense_amount.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        summary_grid.addWidget(QLabel("Income Transactions"), 0, 0)
        summary_grid.addWidget(self.income_count_label, 0, 1)

        summary_grid.addWidget(QLabel("Expense Transactions"), 1, 0)
        summary_grid.addWidget(self.expense_count_label, 1, 1)

        summary_grid.addWidget(QLabel("Highest Income"), 2, 0)
        summary_grid.addWidget(self.highest_income_label, 2, 1)

        summary_grid.addWidget(QLabel("Income Amount"), 3, 0)
        summary_grid.addWidget(self.highest_income_amount, 3, 1)

        summary_grid.addWidget(QLabel("Highest Expense"), 4, 0)
        summary_grid.addWidget(self.highest_expense_label, 4, 1)

        summary_grid.addWidget(QLabel("Expense Amount"), 5, 0)
        summary_grid.addWidget(self.highest_expense_amount, 5, 1)

        for row in range(6):
            summary_grid.setRowStretch(row, 1)

        summary_grid.setColumnStretch(0, 1)
        summary_grid.setColumnStretch(1, 1)

        for row in range(6):
            label = summary_grid.itemAtPosition(row, 0).widget()
            label.setObjectName("summaryLabel")

        summary_layout.addLayout(summary_grid)
        main_layout.addWidget(summary_frame)

    def load_dashboard(self):

        today = date.today()

        income = self.transaction_controller.get_today_income(today)

        expense = self.transaction_controller.get_today_expense(today)

        profit = income - expense

        cash_income = self.transaction_controller.get_cash_income(today)

        cash_expense = self.transaction_controller.get_cash_expense(today)

        online_income = (self.transaction_controller.get_online_income(today))

        online_expense = (self.transaction_controller.get_online_expense(today))

        income_count = (self.transaction_controller.get_income_transaction_count(today))

        expense_count = (self.transaction_controller.get_expense_transaction_count(today))

        highest_income = (self.transaction_controller.get_highest_income_transaction(today))

        highest_expense = (self.transaction_controller.get_highest_expense_transaction(today))

        self.income_count_label.setText(
            str(income_count)
        )

        self.expense_count_label.setText(
            str(expense_count)
        )

        self.income_card.set_value(
            f"₹ {income:.2f}"
        )

        self.expense_card.set_value(
            f"₹ {expense:.2f}"
        )

        self.profit_card.set_value(
            f"₹ {profit:.2f}"
        )

        self.cash_income_card.set_value(
            f"₹ {cash_income:.2f}"
        )

        self.cash_expense_card.set_value(
            f"₹ {cash_expense:.2f}"
        )

        self.online_income_card.set_value(
            f"₹ {online_income:.2f}"
        )

        self.online_expense_card.set_value(
            f"₹ {online_expense:.2f}"
        )

        if highest_income:

            self.highest_income_label.setText(
                f"{highest_income.category.name} ({highest_income.payment_method.name})"
            )

            self.highest_income_amount.setText(
                f"₹ {highest_income.amount:.2f}"
            )

        else:

            self.highest_income_label.setText("-")
            self.highest_income_amount.setText("₹0.00")

        if highest_expense:

            self.highest_expense_label.setText(
                f"{highest_expense.category.name} ({highest_expense.payment_method.name})"
            )

            self.highest_expense_amount.setText(
                f"₹ {highest_expense.amount:.2f}"
            )

        else:

            self.highest_expense_label.setText("-")
            self.highest_expense_amount.setText("₹0.00")
