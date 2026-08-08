from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QMessageBox
from sqlalchemy.exc import SQLAlchemyError

from app.views.main_window import MainWindow
from app.database.session import get_session
from app.database.seed import seed_database
from app.database.init_db import create_tables
from app.utils.logger import logger


def handle_unexpected_exception(exc_type, exc_value, exc_traceback):
    """Log unexpected GUI errors without exposing technical details to users."""

    logger.error(
        "Unexpected application error.",
        exc_info=(exc_type, exc_value, exc_traceback),
    )
    QMessageBox.critical(
        None,
        "Unexpected Error",
        "Something unexpected happened. Please try again.",
    )


def load_theme(app: QApplication):
    theme_path = Path("styles") / "dark.qss"

    if theme_path.exists():
        with open(theme_path, "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())


def run():
    app = QApplication(sys.argv)
    sys.excepthook = handle_unexpected_exception

    app.setApplicationName("Hotel Expense Tracker")

    session = None
    try:
        load_theme(app)
        create_tables()
        session = get_session()
        seed_database(session)

        window = MainWindow(session)
        window.show()
        return app.exec()
    except SQLAlchemyError:
        logger.exception("Database error during application startup.")
        QMessageBox.critical(
            None,
            "Database Error",
            "Unable to connect to the database. Please check the database connection and try again.",
        )
        return 1
    finally:
        if session is not None:
            session.close()
