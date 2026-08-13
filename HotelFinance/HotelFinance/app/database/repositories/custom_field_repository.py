from app.database.repositories.base_repository import BaseRepository
from app.models.custom_field import CustomField


class CustomFieldRepository(BaseRepository):

    def get_all(self):
        return (
            self.session.query(CustomField)
            .order_by(CustomField.name)
            .all()
        )

    def get_by_id(self, field_id):
        return (
            self.session.query(CustomField)
            .filter(CustomField.id == field_id)
            .first()
        )

    def get_by_name(self, name):
        return (
            self.session.query(CustomField)
            .filter(CustomField.name == name)
            .first()
        )

    def add_field(self, name, value):
        field = CustomField(
            name=name,
            value=value,
        )

        return self.add(field)

    def delete_field(self, field):
        return self.delete(field)