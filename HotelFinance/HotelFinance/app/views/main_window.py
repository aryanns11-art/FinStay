from PySide6.QtWidgets import (QHBoxLayout, QMainWindow, QStackedWidget, QVBoxLayout, QWidget)

from app.views.widgets.scrollable_page import ScrollablePage
from app.views.widgets.sidebar import Sidebar
from app.views.widgets.topbar import TopBar
from app.views.widgets.statusbar import StatusBar

from app.views.pages.dashboard_page import DashboardPage
from app.views.pages.transaction_page import TransactionPage
from app.views.pages.cash_page import CashPage
from app.views.pages.reports_page import ReportsPage
from app.views.pages.settings_page import SettingsPage
from app.controllers.settings_controller import SettingsController


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self,session):
        super().__init__()

        self.session = session
        self.settings_controller = SettingsController(session)
        self.hotel_name = self.get_hotel_name()

        self.setWindowTitle(self.hotel_name)
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
        self.sidebar = Sidebar(self.hotel_name)
        main_layout.addWidget(self.sidebar)

        # Right side
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.topbar = TopBar(self.hotel_name)
        right_layout.addWidget(self.topbar)

        self.stack = QStackedWidget()
        right_layout.addWidget(self.stack)

        right_container = QWidget()
        right_container.setLayout(right_layout)

        main_layout.addWidget(right_container)
        main_layout.setStretch(1, 1)

        self.dashboard_page = ScrollablePage(DashboardPage(self.session))
        self.transaction_page = ScrollablePage(TransactionPage(self.session))
        self.cash_page = ScrollablePage(CashPage(self.session))
        self.reports_page = ScrollablePage(ReportsPage(self.session))
        self.settings_page = ScrollablePage(SettingsPage(self.session))

        self.settings_page.hotel_information_saved.connect(self.update_hotel_branding)

        self.transaction_page.transactions_changed.connect(self.dashboard_page.load_dashboard)
        self.transaction_page.transactions_changed.connect(self.cash_page.load_page)
        self.transaction_page.transactions_changed.connect(self.reports_page.generate_report)

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
        self.sidebar.dashboard_btn.clicked.connect(lambda: self.change_page(0))

        self.sidebar.transactions_btn.clicked.connect(lambda: self.change_page(1))

        self.sidebar.cash_btn.clicked.connect(lambda: self.change_page(2))

        self.sidebar.reports_btn.clicked.connect(lambda: self.change_page(3))

        self.sidebar.settings_btn.clicked.connect(lambda: self.change_page(4))

    def get_hotel_name(self):
        return self.settings_controller.get_hotel_name() or "Hotel Expense Tracker"

    def update_hotel_branding(self, hotel_name):
        self.hotel_name = hotel_name or "Hotel Expense Tracker"
        self.setWindowTitle(self.hotel_name)
        self.sidebar.set_hotel_name(self.hotel_name)
        self.topbar.set_hotel_name(self.hotel_name)

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

    def closeEvent(self, event):
        if hasattr(self, "settings_page") and self.settings_page is not None:
            self.settings_page.close_restore_worker()

        super().closeEvent(event)
