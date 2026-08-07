from app.database.repositories.backup_repository import (BackupRepository,)


class BackupService:
    """Business logic for database backup."""

    def __init__(self):
        self.repository = BackupRepository()

    def backup_database(self):
        return self.repository.backup_database()

    def restore_database(self, backup_file):
        self.repository.restore_database(backup_file)

    def get_last_backup(self):
        return self.repository.get_last_backup()

    def get_all_backups(self):
        return self.repository.get_all_backups()