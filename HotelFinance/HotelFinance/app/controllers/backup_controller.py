from app.database.repositories.backup_repository import BackupRepository


class BackupController:
    """Controller for database backup and restore operations."""

    def __init__(self):
        self.repository = BackupRepository()

    # =====================================================
    # Backup
    # =====================================================

    def backup_database(self):
        """Create a PostgreSQL database backup."""

        return self.repository.create_backup()

    # =====================================================
    # Restore
    # =====================================================

    def restore_database(self, backup_file):
        """Restore the database from a backup file."""

        return self.repository.restore_backup(
            backup_file
        )

    # =====================================================
    # Last Backup
    # =====================================================

    def get_last_backup(self):
        """Get the most recent backup file."""

        return self.repository.get_last_backup()