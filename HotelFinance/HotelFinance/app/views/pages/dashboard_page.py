from datetime import datetime

from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
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

        # =====================================================
        # Recent Transactions
        # =====================================================

        section_title = QLabel("Recent Transactions")
        section_title.setObjectName("sectionTitle")

        main_layout.addWidget(section_title)

        self.transaction_table = TransactionTable()
        main_layout.addWidget(self.transaction_table)