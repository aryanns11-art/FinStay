from app.services.category_service import CategoryService


class CategoryController:
    """Controller for categories."""

    def __init__(self, session):
        self.service = CategoryService(session)

    def get_categories(self):
        return self.service.get_categories()