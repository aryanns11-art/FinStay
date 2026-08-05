from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication

from app.views.main_window import MainWindow


def load_theme(app: QApplication):
    theme_path = Path("styles") / "dark.qss"

    if theme_path.exists():
        with open(theme_path, "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())


def run():
    app = QApplication(sys.argv)

    app.setApplicationName("Hotel Expense Tracker")

    load_theme(app)

    window = MainWindow()
    window.show()

    return app.exec()