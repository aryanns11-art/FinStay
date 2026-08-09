import os

from PySide6.QtCore import QThread, Signal

from app.database.repositories.backup_repository import BackupRepository


class RestoreWorker(QThread):
    """Run SQLite restore in a background thread."""

    restore_finished = Signal()
    restore_error = Signal(str)
    restore_done = Signal()

    def __init__(self, backup_file):
        super().__init__()

        self.backup_file = backup_file
        self._cancelled = False

    def run(self):

        try:

            if self._cancelled:
                return

            if not os.path.isfile(self.backup_file):
                raise FileNotFoundError(
                    "Selected backup file does not exist."
                )

            repository = BackupRepository()
            repository.restore_backup(self.backup_file)

            if self._cancelled:
                return

            self.restore_finished.emit()

        except Exception as error:

            self.restore_error.emit(
                str(error)
            )

        finally:
            self.restore_done.emit()

    def stop(self):
        """Request cancellation of the restore worker."""

        self._cancelled = True

        if self.isRunning():
            self.wait(5000)
