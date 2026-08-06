from datetime import datetime, date

from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from app.views.widgets.stat_card import StatCard
from app.views.widgets.transaction_table import TransactionTable

from app.controllers.transaction_controller import (TransactionController,)

class DashboardPage(QWidget):
    """Dashboard page."""

    def __init__(self,session):
        super().__init__()

        self.session = session

        self.transaction_controller = TransactionController(session)

        self.init_ui()

        self.load_dashboard()


    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # =====================================================
        # Header
        # =====================================================

        header_layout = QHBoxLayout()

        title = QLabel("Dashboard")
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
        # Statistics Cards
        # =====================================================

        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)

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
        # Recent Transactions
        # =====================================================

        section_title = QLabel("Recent Transactions")
        section_title.setObjectName("sectionTitle")

        main_layout.addWidget(section_title)

        self.transaction_table = TransactionTable()
        main_layout.addWidget(self.transaction_table)

    def load_dashboard(self):

        today = date.today()

        income = self.transaction_controller.get_today_income(today)

        expense = self.transaction_controller.get_today_expense(today)

        profit = income - expense

        cash_income = self.transaction_controller.get_cash_income(today)

        cash_expense = self.transaction_controller.get_cash_expense(today)

        online_income = (self.transaction_controller.get_online_income(today))

        online_expense = (self.transaction_controller.get_online_expense(today))

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