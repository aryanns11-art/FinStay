from datetime import datetime
import re

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import ( QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QMessageBox, QFileDialog, QProgressDialog)
from sqlalchemy.exc import SQLAlchemyError

from app.controllers.backup_controller import BackupController
from app.controllers.settings_controller import SettingsController
from app.workers.restore_worker import RestoreWorker
from app.database.connection import engine


class SettingsPage(QWidget):

    hotel_information_saved = Signal(str)

    def __init__(self, session):
        super().__init__()

        self.session = session
        self.backup_controller = BackupController()
        self.settings_controller = SettingsController(session)
        self.restore_worker = None
        self.restore_progress = None

        self.init_ui()
        self.load_hotel_information()
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

        hotel_title = QLabel("Hotel Information")
        hotel_title.setObjectName("sectionTitle")
        main_layout.addWidget(hotel_title)

        hotel_card = QFrame()
        hotel_card.setObjectName("chartCard")
        hotel_card.setFrameShape(QFrame.StyledPanel)
        hotel_card.setLineWidth(1)

        hotel_layout = QGridLayout(hotel_card)
        hotel_layout.setContentsMargins(20, 20, 20, 20)
        hotel_layout.setSpacing(12)

        self.hotel_name_edit = QLineEdit()
        self.hotel_name_edit.setPlaceholderText("Hotel Name")
        self.hotel_address_edit = QLineEdit()
        self.hotel_address_edit.setPlaceholderText("Hotel Address")
        self.phone_number_edit = QLineEdit()
        self.phone_number_edit.setPlaceholderText("Phone Number")
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Email Address")
        self.gstin_edit = QLineEdit()
        self.gstin_edit.setPlaceholderText("GSTIN (Optional)")

        hotel_layout.addWidget(QLabel("Hotel Name *"), 0, 0)
        hotel_layout.addWidget(self.hotel_name_edit, 0, 1, 1, 3)
        hotel_layout.addWidget(QLabel("Hotel Address"), 1, 0)
        hotel_layout.addWidget(self.hotel_address_edit, 1, 1, 1, 3)
        hotel_layout.addWidget(QLabel("Phone Number"), 2, 0)
        hotel_layout.addWidget(self.phone_number_edit, 2, 1)
        hotel_layout.addWidget(QLabel("Email Address"), 2, 2)
        hotel_layout.addWidget(self.email_edit, 2, 3)
        hotel_layout.addWidget(QLabel("GSTIN"), 3, 0)
        hotel_layout.addWidget(self.gstin_edit, 3, 1, 1, 3)

        save_layout = QHBoxLayout()
        save_layout.addStretch()
        self.save_hotel_information_button = QPushButton("Save Changes")
        self.save_hotel_information_button.clicked.connect(self.save_hotel_information)
        save_layout.addWidget(self.save_hotel_information_button)
        hotel_layout.addLayout(save_layout, 4, 0, 1, 4)

        hotel_layout.setColumnStretch(1, 1)
        hotel_layout.setColumnStretch(3, 1)
        main_layout.addWidget(hotel_card)

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

        self.last_backup_label = QLabel("Never")

        rows = [
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
        self.restore_button.setObjectName("dangerButton")

        self.backup_button.clicked.connect(self.backup_database)
        self.restore_button.clicked.connect(self.restore_database)

        buttons_layout.addWidget(self.backup_button)
        buttons_layout.addWidget(self.restore_button)
        buttons_layout.addStretch()

        backup_card_layout.addLayout(buttons_layout)

        main_layout.addWidget(backup_card)
        main_layout.addStretch(1)

    def load_hotel_information(self):
        """Populate hotel information fields from the settings record."""

        try:
            settings = self.settings_controller.get_settings()
        except SQLAlchemyError:
            QMessageBox.critical(
                self,
                "Database Error",
                "Unable to load hotel information. Please check the database connection and try again.",
            )
            return

        if settings is None:
            return

        self.hotel_name_edit.setText(settings.hotel_name or "")
        self.hotel_address_edit.setText(settings.hotel_address or "")
        self.phone_number_edit.setText(settings.phone_number or "")
        self.email_edit.setText(settings.email or "")
        self.gstin_edit.setText(settings.gstin or "")

    def save_hotel_information(self):
        """Validate and persist hotel information in the settings record."""

        hotel_name = self.hotel_name_edit.text().strip()
        hotel_address = self.hotel_address_edit.text().strip()
        phone_number = self.phone_number_edit.text().strip()
        email = self.email_edit.text().strip()
        gstin = self.gstin_edit.text().strip()

        if not hotel_name:
            QMessageBox.warning(
                self,
                "Invalid Information",
                "Please enter the hotel name.",
            )
            return

        if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            QMessageBox.warning(
                self,
                "Invalid Information",
                "Please enter a valid email address.",
            )
            return

        try:
            self.settings_controller.save_hotel_information(
                hotel_name,
                hotel_address or None,
                phone_number or None,
                email or None,
                gstin or None,
            )
        except SQLAlchemyError:
            QMessageBox.critical(
                self,
                "Unable to Save Hotel Information",
                "Unable to save hotel information. Please try again.",
            )
            return

        QMessageBox.information(
            self,
            "Saved",
            "Hotel information saved successfully.",
        )
        self.hotel_information_saved.emit(hotel_name)

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
