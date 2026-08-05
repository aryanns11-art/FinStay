from app.database.repositories.base_repository import BaseRepository
from app.models.settings import Settings


class SettingsRepository(BaseRepository):
    """Repository for application settings."""

    def get_settings(self):
        return (
            self.session.query(Settings)
            .first()
        )