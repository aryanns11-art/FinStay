import sqlite3
import time
from datetime import datetime
from pathlib import Path

from config import BACKUP_DIR, DATABASE_PATH


class BackupRepository:
    """Handle SQLite database backup and restore operations."""

    def __init__(self):

        self.backup_directory = Path(BACKUP_DIR)

        self.backup_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # =====================================================
    # Backup
    # =====================================================

    def create_backup(self):
        """Create a consistent SQLite database backup using the online backup API."""

        if not DATABASE_PATH.exists():
            raise RuntimeError(
                "Database file does not exist."
            )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        backup_file = (
            self.backup_directory
            / f"hotel_finance_{timestamp}.db"
        )

        try:
            source = sqlite3.connect(str(DATABASE_PATH))
            try:
                destination = sqlite3.connect(str(backup_file))
                try:
                    source.backup(destination)
                finally:
                    destination.close()
            finally:
                source.close()

        except Exception:
            if backup_file.exists():
                backup_file.unlink()

            raise RuntimeError(
                "Database backup could not be created."
            )

        return backup_file

    # =====================================================
    # Restore
    # =====================================================

    def restore_backup(self, backup_file):
        """
        Restore the SQLite database from a backup file.

        Uses the SQLite online backup API to copy into the live database file.
        This avoids Windows file-lock failures that occur when replacing the
        database file while handles may still be closing.
        """

        backup_file = Path(backup_file)

        if not backup_file.exists():
            raise FileNotFoundError(
                "Selected backup file does not exist."
            )

        self._validate_backup_file(backup_file)

        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

        last_error = None

        for _ in range(15):
            try:
                destination = sqlite3.connect(str(DATABASE_PATH), timeout=30)
                try:
                    source = sqlite3.connect(str(backup_file))
                    try:
                        source.backup(destination)
                        destination.commit()
                    finally:
                        source.close()
                finally:
                    destination.close()

                self._remove_sidecar_files(DATABASE_PATH)
                return True

            except Exception as error:
                last_error = error
                time.sleep(0.2)

        raise RuntimeError(
            "Database restore failed. Please verify the backup file."
        ) from last_error

    # =====================================================
    # Last Backup
    # =====================================================

    def get_last_backup(self):
        """Return the most recently created backup."""

        backups = list(
            self.backup_directory.glob(
                "hotel_finance_*.db"
            )
        )

        if not backups:
            return None

        return max(
            backups,
            key=lambda file: file.stat().st_mtime,
        )

    def get_all_backups(self):
        """Return all backup files sorted newest first."""

        backups = list(
            self.backup_directory.glob(
                "hotel_finance_*.db"
            )
        )

        return sorted(
            backups,
            key=lambda file: file.stat().st_mtime,
            reverse=True,
        )

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _validate_backup_file(backup_file: Path):
        """Ensure the selected file is a readable SQLite database with tables."""

        try:
            connection = sqlite3.connect(
                f"file:{backup_file.as_posix()}?mode=ro",
                uri=True,
            )
            try:
                row = connection.execute(
                    "SELECT count(*) FROM sqlite_master WHERE type='table'"
                ).fetchone()
            finally:
                connection.close()

        except sqlite3.Error as error:
            raise RuntimeError(
                "Database restore failed. Please verify the backup file."
            ) from error

        if not row or row[0] == 0:
            raise RuntimeError(
                "Database restore failed. Please verify the backup file."
            )

    @staticmethod
    def _remove_sidecar_files(database_path: Path):
        """Remove leftover SQLite WAL/SHM files after replacing the database."""

        for suffix in ("-wal", "-shm"):
            sidecar = Path(str(database_path) + suffix)
            if sidecar.exists():
                try:
                    sidecar.unlink()
                except OSError:
                    pass
