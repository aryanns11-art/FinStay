from app.services.category_service import CategoryService


class CategoryController:
    """Controller for categories."""

    def __init__(self, session):
        self.service = CategoryService(session)

    def get_categories(self):
        return self.service.get_categories()

    def create_category(self, name, category_type):
        return self.service.create_category(
            name=name,
            category_type=category_type,
        )