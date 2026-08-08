from app.database.repositories.settings_repository import SettingsRepository


class SettingsService:
    """Business logic for application settings."""

    def __init__(self, session):
        self.repository = SettingsRepository(session)

    def get_settings(self):
        return self.repository.get_settings()

    def get_hotel_name(self):
        settings = self.get_settings()
        return settings.hotel_name if settings and settings.hotel_name else None

    def save_hotel_information(self, hotel_name, hotel_address, phone_number, email, gstin):
        return self.repository.save_hotel_information(
            hotel_name,
            hotel_address,
            phone_number,
            email,
            gstin,
        )
