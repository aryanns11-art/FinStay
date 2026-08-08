from datetime import datetime

from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import ( QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout, QMessageBox, QFileDialog, QProgressDialog)

from app.controllers.backup_controller import BackupController
from app.workers.restore_worker import RestoreWorker
from app.database.connection import engine
from config import DB_NAME


class SettingsPage(QWidget):

    def __init__(self, session):
        super().__init__()

        self.session = session
        self.backup_controller = BackupController()
        self.restore_worker = None
        self.restore_progress = None

        self.init_ui()
        self.load_backup_info()

    def init_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        header_layout = QHBoxLayout()

        title = QLabel("Settings")
        title.setObjectName("pageTitle")

        date_label = QLabel(datetime.now().strftime("%A, %d %b %Y"))
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

        description_label = QLabel("Protect your hotel financial data by creating regular database backups.")
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

        try:
            backup_folder = self.backup_controller.repository.backup_directory
            backup_folder.mkdir(parents=True, exist_ok=True)
            folder_path = backup_folder.resolve()
        except OSError:
            QMessageBox.critical(
                self,
                "Unable to Open Folder",
                "The backup folder could not be accessed. Please try again.",
            )
            return

        if not QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder_path))):
            QMessageBox.warning(
                self,
                "Open Failed",
                "Could not open the backup folder.",
            )

    def backup_database(self):

        try:
            backup_file = (self.backup_controller.backup_database())
            QMessageBox.information(self,"Backup Complete",f"Database backed up successfully.\n\n{backup_file.name}",)
            self.load_backup_info()

        except (OSError, RuntimeError):
            QMessageBox.critical(
                self,
                "Backup Failed",
                "The database backup could not be created. Please check the backup location and try again.",
            )


    def load_backup_info(self):

        backup = (self.backup_controller.get_last_backup())

        if backup:
            last_modified = datetime.fromtimestamp(backup.stat().st_mtime)
            self.last_backup_label.setText(last_modified.strftime("%d %b %Y %I:%M %p"))

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

        # =====================================================
        # Close existing database connections
        # =====================================================

        if self.session is not None:
            self.session.close()

        engine.dispose()

        # =====================================================
        # Disable buttons
        # =====================================================

        self.restore_button.setEnabled(False)
        self.backup_button.setEnabled(False)

        # =====================================================
        # Restore Progress
        # =====================================================

        self.restore_progress = QProgressDialog("Restoring database...\nPlease wait.",None,0,0,self,)

        self.restore_progress.setWindowTitle("Restoring Database")

        self.restore_progress.setWindowModality(Qt.ApplicationModal)

        self.restore_progress.setCancelButton(None)

        self.restore_progress.setMinimumWidth(350)

        self.restore_progress.show()

        # =====================================================
        # Restore Worker
        # =====================================================

        self.restore_worker = RestoreWorker(backup_file)
        self.restore_worker.restore_finished.connect(self.restore_finished)
        self.restore_worker.restore_error.connect(self.restore_failed)
        self.restore_worker.restore_done.connect(self.cleanup_restore_worker)
        self.restore_worker.start()


    def restore_finished(self):

        if self.restore_progress is not None:
            self.restore_progress.close()
            self.restore_progress.deleteLater()
            self.restore_progress = None
    
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

        self.cleanup_restore_worker()


    def restore_failed(self, error):
    
        if self.restore_progress is not None:
            self.restore_progress.close()
            self.restore_progress.deleteLater()
            self.restore_progress = None
    
        self.restore_button.setEnabled(True)
        self.backup_button.setEnabled(True)
    
        QMessageBox.critical(
            self,
            "Restore Failed",
            "The database could not be restored. Please verify the selected backup file and try again.",
        )

        self.cleanup_restore_worker()


    def cleanup_restore_worker(self):
    
        if self.restore_worker is None:
            return
    
        worker = self.restore_worker
        self.restore_worker = None
    
        if worker.isRunning():
            worker.wait(5000)
    
        worker.deleteLater()
    
    
    def close_restore_worker(self):
    
        if self.restore_worker is None:
            return
    
        worker = self.restore_worker
    
        if self.restore_progress is not None:
            self.restore_progress.close()
            self.restore_progress.deleteLater()
            self.restore_progress = None
    
        if worker.isRunning():
            worker.stop()
            worker.wait(5000)
    
        self.restore_worker = None
    
        worker.deleteLater()
