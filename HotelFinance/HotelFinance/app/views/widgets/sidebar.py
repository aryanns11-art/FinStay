from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from app.views.widgets.navigation_button import NavigationButton

class Sidebar(QFrame):

    def __init__(self):
        super().__init__()

        self.setFixedWidth(250)

        self.setObjectName("sidebar")

        layout = QVBoxLayout(self)

        layout.setContentsMargins(15, 20, 15, 20)

        layout.setSpacing(8)

        title = QLabel("Hotel Expense Tracker")

        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        layout.addSpacing(20)

        self.dashboard_btn = NavigationButton(
            "Dashboard",
            "fa5s.home",
        )

        self.transactions_btn = NavigationButton(
            "Transactions",
            "fa5s.wallet",
        )

        self.cash_btn = NavigationButton(
            "Cash Counter",
            "fa5s.cash-register",
        )

        self.reports_btn = NavigationButton(
            "Reports",
            "fa5s.chart-bar",
        )

        self.settings_btn = NavigationButton(
            "Settings",
            "fa5s.cog",
        )

        self.exit_btn = NavigationButton(
            "Exit",
            "fa5s.sign-out-alt",
        )

        self.dashboard_btn.setChecked(True)

        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.transactions_btn)
        layout.addWidget(self.cash_btn)
        layout.addWidget(self.reports_btn)
        layout.addWidget(self.settings_btn)

        layout.addStretch()

        layout.addWidget(self.exit_btn)
