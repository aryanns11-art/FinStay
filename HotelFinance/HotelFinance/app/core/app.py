from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication

from app.views.main_window import MainWindow
from app.database.session import get_session
from app.database.seed import seed_database
from app.database.init_db import create_tables


def load_theme(app: QApplication):
    theme_path = Path("styles") / "dark.qss"

    if theme_path.exists():
        with open(theme_path, "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())


def run():
    app = QApplication(sys.argv)

    app.setApplicationName("Hotel Expense Tracker")

    load_theme(app)

    create_tables()

    # Create one database session for the application   
    session = get_session()
    seed_database(session)

    window = MainWindow(session)
    window.show()

    exit_code = app.exec()

    session.close()

    return exit_code