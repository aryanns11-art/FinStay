from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.views.pages.dashboard_page import DashboardPage
from app.views.widgets.sidebar import Sidebar
from app.views.widgets.statusbar import StatusBar
from app.views.widgets.topbar import TopBar


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

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

        self.stack.addWidget(DashboardPage())

        self.setStatusBar(StatusBar())