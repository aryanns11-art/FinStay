from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.views.widgets.sidebar import Sidebar
from app.views.widgets.topbar import TopBar
from app.views.widgets.statusbar import StatusBar

from app.views.pages.dashboard_page import DashboardPage
from app.views.pages.transaction_page import TransactionPage
from app.views.pages.cash_page import CashPage
from app.views.pages.reports_page import ReportsPage
from app.views.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self,session):
        super().__init__()

        self.session = session

        self.setWindowTitle("Hotel Expense Tracker")
        self.resize(1600, 900)
        self.setMinimumSize(1400, 850)

        self.init_ui()

    def init_ui(self):
        # Main container
        central = QWidget()
        self.setCentralWidget(central)

        # Main horizontal layout
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # Right side
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.topbar = TopBar()
        right_layout.addWidget(self.topbar)

        self.stack = QStackedWidget()
        right_layout.addWidget(self.stack)

        right_container = QWidget()
        right_container.setLayout(right_layout)

        main_layout.addWidget(right_container)
        main_layout.setStretch(1, 1)

        self.dashboard_page = DashboardPage()
        self.transaction_page = TransactionPage(self.session)
        self.cash_page = CashPage()
        self.reports_page = ReportsPage()
        self.settings_page = SettingsPage()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.transaction_page)
        self.stack.addWidget(self.cash_page)
        self.stack.addWidget(self.reports_page)
        self.stack.addWidget(self.settings_page)
        
        self.stack.setCurrentIndex(0)

        self.statusbar = StatusBar()
        self.setStatusBar(self.statusbar)

        self.connect_signals()

    def connect_signals(self):
        self.sidebar.dashboard_btn.clicked.connect(
            lambda: self.change_page(0)
        )

        self.sidebar.transactions_btn.clicked.connect(
            lambda: self.change_page(1)
        )

        self.sidebar.cash_btn.clicked.connect(
            lambda: self.change_page(2)
        )

        self.sidebar.reports_btn.clicked.connect(
            lambda: self.change_page(3)
        )

        self.sidebar.settings_btn.clicked.connect(
            lambda: self.change_page(4)
        )

    def change_page(self, index: int):
        self.stack.setCurrentIndex(index)

        buttons = [
            self.sidebar.dashboard_btn,
            self.sidebar.transactions_btn,
            self.sidebar.cash_btn,
            self.sidebar.reports_btn,
            self.sidebar.settings_btn,
        ]

        for button in buttons:
            button.setChecked(False)

        buttons[index].setChecked(True)