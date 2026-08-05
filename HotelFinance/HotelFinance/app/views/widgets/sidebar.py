from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

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

        self.dashboard = NavigationButton(
            "Dashboard",
            "fa5s.home",
        )

        self.transaction = NavigationButton(
            "Transactions",
            "fa5s.wallet",
        )

        self.cash = NavigationButton(
            "Cash Counter",
            "fa5s.money-bill-wave",
        )

        self.report = NavigationButton(
            "Reports",
            "fa5s.chart-bar",
        )

        self.settings = NavigationButton(
            "Settings",
            "fa5s.cog",
        )

        self.exit = NavigationButton(
            "Exit",
            "fa5s.sign-out-alt",
        )

        self.dashboard.setChecked(True)

        layout.addWidget(self.dashboard)
        layout.addWidget(self.transaction)
        layout.addWidget(self.cash)
        layout.addWidget(self.report)
        layout.addWidget(self.settings)

        layout.addStretch()

        layout.addWidget(self.exit)