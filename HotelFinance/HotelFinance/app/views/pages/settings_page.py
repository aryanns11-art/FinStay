from datetime import datetime

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGridLayout,
    QMessageBox,
    QFileDialog,
)

from app.controllers.backup_controller import BackupController
from app.workers.restore_worker import RestoreWorker
from app.database.connection import engine
from config import DB_NAME


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.backup_controller = BackupController()

        self.init_ui()
        self.load_backup_info()

    def init_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        header_layout = QHBoxLayout()

        title = QLabel("Settings")
        title.setObjectName("pageTitle")

        date_label = QLabel(
            datetime.now().strftime("%A, %d %b %Y")
        )
        date_label.setObjectName("dateLabel")

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(date_label)

        main_layout.addLayout(header_layout)

        section_title = QLabel("Backup & Restore")
        section_title.setObjectName("sectionTitle")
        main_layout.addWidget(section_title)

        backup_card = QFrame()
        backup_card.setObjectName("chartCard")
        backup_card.setFrameShape(QFrame.StyledPanel)
        backup_card.setLineWidth(1)

        backup_card_layout = QVBoxLayout(backup_card)
        backup_card_layout.setContentsMargins(20, 20, 20, 20)
        backup_card_layout.setSpacing(16)

        description_label = QLabel(
            "Protect your hotel financial data by creating regular database backups."
        )
        description_label.setObjectName("descriptionLabel")
        description_label.setWordWrap(True)
        backup_card_layout.addWidget(description_label)

        info_grid = QGridLayout()
        info_grid.setSpacing(10)

        self.status_label = QLabel("Connected")
        self.status_label.setObjectName("statusBadge")

        self.database_type_label = QLabel("PostgreSQL")
        self.database_name_label = QLabel(DB_NAME or "hotel_finance")
        self.last_backup_label = QLabel("Never")

        rows = [
            ("Database Status", self.status_label),
            ("Database Type", self.database_type_label),
            ("Database Name", self.database_name_label),
            ("Last Backup", self.last_backup_label),
        ]

        for row_index, (label_text, value_widget) in enumerate(rows):
            label = QLabel(label_text)
            label.setWordWrap(True)
            info_grid.addWidget(label, row_index, 0)
            info_grid.addWidget(value_widget, row_index, 1)

        info_grid.setColumnStretch(0, 1)
        info_grid.setColumnStretch(1, 2)
        backup_card_layout.addLayout(info_grid)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.backup_button = QPushButton("Backup Database")
        self.restore_button = QPushButton("Restore Database")

        self.backup_button.clicked.connect(self.backup_database)
        self.restore_button.clicked.connect(self.restore_database)

        buttons_layout.addWidget(self.backup_button)
        buttons_layout.addWidget(self.restore_button)
        buttons_layout.addStretch()

        backup_card_layout.addLayout(buttons_layout)

        main_layout.addWidget(backup_card)

        location_title = QLabel("Backup Location")
        location_title.setObjectName("sectionTitle")
        main_layout.addWidget(location_title)

        location_card = QFrame()
        location_card.setObjectName("chartCard")
        location_card.setFrameShape(QFrame.StyledPanel)
        location_card.setLineWidth(1)

        location_card_layout = QVBoxLayout(location_card)
        location_card_layout.setContentsMargins(20, 20, 20, 20)
        location_card_layout.setSpacing(12)

        location_description = QLabel(
            "Backups are stored locally on this computer."
        )
        location_description.setWordWrap(True)
        location_card_layout.addWidget(location_description)

        backup_folder = self.backup_controller.repository.backup_directory
        backup_folder_path = (
            f"{backup_folder.as_posix()}/"
            if str(backup_folder)
            else "backups/"
        )

        self.backup_path_label = QLabel(backup_folder_path)
        self.backup_path_label.setWordWrap(True)
        location_card_layout.addWidget(self.backup_path_label)

        open_folder_row = QHBoxLayout()
        self.open_backup_folder_button = QPushButton("Open Backup Folder")
        self.open_backup_folder_button.clicked.connect(self.open_backup_folder)
        open_folder_row.addWidget(self.open_backup_folder_button)
        open_folder_row.addStretch()
        location_card_layout.addLayout(open_folder_row)

        main_layout.addWidget(location_card)
        main_layout.addStretch(1)

    def open_backup_folder(self):

        backup_folder = self.backup_controller.repository.backup_directory
        backup_folder.mkdir(parents=True, exist_ok=True)

        folder_path = backup_folder.resolve()

        if not QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder_path))):
            QMessageBox.warning(
                self,
                "Open Failed",
                "Could not open the backup folder.",
            )

    def backup_database(self):

        try:

            backup_file = (
                self.backup_controller.backup_database()
            )

            QMessageBox.information(
                self,
                "Backup Complete",
                f"Database backed up successfully.\n\n{backup_file.name}",
            )

            self.load_backup_info()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Backup Failed",
                str(error),
            )

    def load_backup_info(self):

        backup = (
            self.backup_controller.get_last_backup()
        )

        if backup:

            last_modified = datetime.fromtimestamp(
                backup.stat().st_mtime
            )

            self.last_backup_label.setText(
                last_modified.strftime(
                    "%d %b %Y %I:%M %p"
                )
            )

        else:

            self.last_backup_label.setText("Never")

    def restore_database(self):

        backup_file, _ = QFileDialog.getOpenFileName(
            self,
            "Select PostgreSQL Backup",
            str(
                self.backup_controller
                .repository
                .backup_directory
            ),
            "PostgreSQL Backup (*.backup);;All Files (*)",
        )

        if not backup_file:
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Restore",
            (
                "Restoring this backup will replace the "
                "current database data.\n\n"
                "Are you sure you want to continue?"
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirm != QMessageBox.Yes:
            return

        engine.dispose()

        self.restore_button.setEnabled(False)
        self.backup_button.setEnabled(False)

        self.restore_worker = RestoreWorker(
            backup_file
        )

        self.restore_worker.finished.connect(
            self.restore_finished
        )

        self.restore_worker.error.connect(
            self.restore_failed
        )

        self.restore_worker.start()

    def restore_finished(self):

        self.restore_button.setEnabled(True)
        self.backup_button.setEnabled(True)

        QMessageBox.information(
            self,
            "Restore Complete",
            (
                "Database restored successfully.\n\n"
                "Please restart the application "
                "to reload the restored data."
            ),
        )

    def restore_failed(self, error):

        self.restore_button.setEnabled(True)
        self.backup_button.setEnabled(True)

        QMessageBox.critical(
            self,
            "Restore Failed",
            error,
        )

    def close_restore_worker(self):

        if hasattr(self, "restore_worker"):

            if self.restore_worker.isRunning():

                self.restore_worker.stop()
