from PySide6.QtWidgets import (
    QHBoxLayout,
    QFrame,
    QLabel,
    QVBoxLayout,
)
from PySide6.QtCore import QSize
import qtawesome as qta

from app.views.widgets.navigation_button import NavigationButton

class Sidebar(QFrame):

    def __init__(self, hotel_name="Hotel Expense Tracker"):
        super().__init__()

        self.setFixedWidth(250)

        self.setObjectName("sidebar")

        layout = QVBoxLayout(self)

        layout.setContentsMargins(15, 20, 15, 20)

        layout.setSpacing(8)

        brand_layout = QHBoxLayout()
        brand_layout.setSpacing(8)

        brand_mark = QLabel()
        brand_mark.setObjectName("sidebarMark")
        brand_mark.setPixmap(qta.icon("fa5s.hotel", color="#D4AF37").pixmap(QSize(18, 18)))

        self.title_label = QLabel(hotel_name)
        self.title_label.setObjectName("sidebarBrand")

        brand_layout.addWidget(brand_mark)
        brand_layout.addWidget(self.title_label)
        brand_layout.addStretch()
        layout.addLayout(brand_layout)

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
            "Cash Management",
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

        self.dashboard_btn.setChecked(True)

        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.transactions_btn)
        layout.addWidget(self.cash_btn)
        layout.addWidget(self.reports_btn)
        layout.addWidget(self.settings_btn)

        layout.addStretch()

    def set_hotel_name(self, hotel_name):
        self.title_label.setText(hotel_name)
