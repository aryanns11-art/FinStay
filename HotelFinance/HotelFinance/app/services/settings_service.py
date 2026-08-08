from app.database.repositories.settings_repository import SettingsRepository


class SettingsService:
    """Business logic for application settings."""

    def __init__(self, session):
        self.repository = SettingsRepository(session)

    def get_settings(self):
        return self.repository.get_settings()

    def save_hotel_information(self, hotel_name, hotel_address, phone_number, email, gstin):
        return self.repository.save_hotel_information(
            hotel_name,
            hotel_address,
            phone_number,
            email,
            gstin,
        )
