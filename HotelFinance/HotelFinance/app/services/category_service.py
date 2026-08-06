from app.database.repositories.category_repository import CategoryRepository


class CategoryService:
    """Business logic for categories."""

    def __init__(self, session):
        self.repository = CategoryRepository(session)

    def get_categories(self):
        return self.repository.get_all()