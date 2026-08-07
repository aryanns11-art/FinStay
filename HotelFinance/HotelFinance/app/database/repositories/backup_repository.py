import os
import subprocess
from datetime import datetime
from pathlib import Path

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)

from app.utils.postgres_tools import PostgreSQLTools


class BackupRepository:
    """Handle PostgreSQL database backup and restore operations."""

    def __init__(self):

        self.backup_directory = Path("backups")

        self.backup_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # =====================================================
    # Backup
    # =====================================================

    def create_backup(self):
        """Create a PostgreSQL database backup."""

        pg_dump = PostgreSQLTools.find_pg_dump()

        if not pg_dump:
            raise RuntimeError(
                "pg_dump.exe could not be found."
            )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        backup_file = (
            self.backup_directory
            / f"hotel_finance_{timestamp}.backup"
        )

        environment = os.environ.copy()

        environment["PGPASSWORD"] = DB_PASSWORD

        command = [
            str(pg_dump),

            "--host",
            DB_HOST,

            "--port",
            str(DB_PORT),

            "--username",
            DB_USER,

            "--dbname",
            DB_NAME,

            "--format",
            "custom",

            "--file",
            str(backup_file),
        ]

        result = subprocess.run(
            command,
            env=environment,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:

            if backup_file.exists():
                backup_file.unlink()

            raise RuntimeError(
                result.stderr.strip()
                or "Database backup failed."
            )

        return backup_file

    # =====================================================
    # Restore
    # =====================================================

    def restore_backup(self, backup_file):
        """Restore PostgreSQL database from a backup file."""

        pg_restore = PostgreSQLTools.find_pg_restore()

        if not pg_restore:
            raise RuntimeError(
                "pg_restore.exe could not be found."
            )

        backup_file = Path(backup_file)

        if not backup_file.exists():
            raise FileNotFoundError(
                "Selected backup file does not exist."
            )

        environment = os.environ.copy()

        environment["PGPASSWORD"] = DB_PASSWORD

        command = [
            str(pg_restore),

            "--host",
            DB_HOST,

            "--port",
            str(DB_PORT),

            "--username",
            DB_USER,

            "--dbname",
            DB_NAME,

            "--clean",

            "--if-exists",

            "--no-owner",

            str(backup_file),
        ]

        result = subprocess.run(
            command,
            env=environment,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:

            raise RuntimeError(
                result.stderr.strip()
                or "Database restore failed."
            )

        return True

    # =====================================================
    # Last Backup
    # =====================================================

    def get_last_backup(self):
        """Return the most recently created backup."""

        backups = list(
            self.backup_directory.glob(
                "hotel_finance_*.backup"
            )
        )

        if not backups:
            return None

        return max(
            backups,
            key=lambda file: file.stat().st_mtime,
        )