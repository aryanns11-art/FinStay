from app.services.settings_service import SettingsService


class SettingsController:
    """Coordinates application settings operations."""

    def __init__(self, session):
        self.service = SettingsService(session)

    def get_settings(self):
        return self.service.get_settings()

    def get_hotel_name(self):
        return self.service.get_hotel_name()

    def save_hotel_information(self, hotel_name, hotel_address, phone_number, email, gstin):
        return self.service.save_hotel_information(
            hotel_name,
            hotel_address,
            phone_number,
            email,
            gstin,
        )
