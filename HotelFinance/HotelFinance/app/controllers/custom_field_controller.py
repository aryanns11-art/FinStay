from app.services.custom_field_service import CustomFieldService


class CustomFieldController:

    def __init__(self, session):
        self.service = CustomFieldService(session)

    def get_all(self):
        return self.service.get_all()

    def add_field(self, name, value):
        return self.service.add_field(name, value)

    def delete_field(self, field_id):
        return self.service.delete_field(field_id)