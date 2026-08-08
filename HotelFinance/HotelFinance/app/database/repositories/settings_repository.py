from app.database.repositories.base_repository import BaseRepository
from app.models.settings import Settings


class SettingsRepository(BaseRepository):
    """Repository for application settings."""

    def get_settings(self):
        return (
            self.session.query(Settings)
            .first()
        )

    def save_hotel_information(self, hotel_name, hotel_address, phone_number, email, gstin):
        settings = self.get_settings()

        if settings is None:
            settings = Settings()

        settings.hotel_name = hotel_name
        settings.hotel_address = hotel_address
        settings.phone_number = phone_number
        settings.email = email
        settings.gstin = gstin

        if settings.id is None:
            return self.add(settings)

        self.update()
        return settings
