from app.database.repositories.custom_field_repository import (
    CustomFieldRepository,
)


class CustomFieldService:

    def __init__(self, session):
        self.repository = CustomFieldRepository(session)

    def get_all(self):
        return self.repository.get_all()

    def add_field(self, name, value):
        name = name.strip()
        value = value.strip()

        if not name:
            raise ValueError("Field name is required.")

        if not value:
            raise ValueError("Field value is required.")

        existing = self.repository.get_by_name(name)

        if existing:
            raise ValueError(
                f"A field named '{name}' already exists."
            )

        return self.repository.add_field(name, value)

    def delete_field(self, field_id):
        field = self.repository.get_by_id(field_id)

        if not field:
            raise ValueError("Custom field not found.")

        return self.repository.delete_field(field)