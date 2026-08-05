from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from app.views.widgets.stat_card import StatCard

from app.views.widgets.transaction_table import TransactionTable

class DashboardPage(QWidget):
    """Dashboard page."""

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Dashboard Title
        title = QLabel("Dashboard                                                           Thursday, 06 Aug 2026")
        title.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
            margin-bottom:10px;
        """)
        main_layout.addWidget(title)

        # =======================
        # Statistics Cards
        # =======================

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
            "Profit",
            "₹0",
        )

        self.cash_card = StatCard(
            "Cash In Hand",
            "₹0",
        )

        stats_layout.addWidget(self.income_card, 0, 0)
        stats_layout.addWidget(self.expense_card, 0, 1)
        stats_layout.addWidget(self.profit_card, 0, 2)
        stats_layout.addWidget(self.cash_card, 0, 3)

        main_layout.addLayout(stats_layout)

        # =======================
        # Recent Transactions
        # =======================

        section_title = QLabel("Recent Transactions")
        section_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            margin-top:20px;
            margin-bottom:8px;
        """)

        main_layout.addWidget(section_title)

        self.transaction_table = TransactionTable()
        main_layout.addWidget(self.transaction_table)