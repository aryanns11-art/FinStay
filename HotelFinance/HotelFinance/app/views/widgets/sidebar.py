from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from app.views.widgets.navigation_button import NavigationButton

class Sidebar(QFrame):

    def __init__(self, hotel_name="Hotel Expense Tracker"):
        super().__init__()

        self.setFixedWidth(250)

        self.setObjectName("sidebar")

        layout = QVBoxLayout(self)

        layout.setContentsMargins(15, 20, 15, 20)

        layout.setSpacing(8)

        self.title_label = QLabel(hotel_name)

        self.title_label.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        layout.addWidget(self.title_label)

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

    def set_hotel_name(self, hotel_name):
        self.title_label.setText(hotel_name)
