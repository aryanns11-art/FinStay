from app.database.repositories.category_repository import CategoryRepository


class CategoryService:
    """Business logic for categories."""

    def __init__(self, session):
        self.repository = CategoryRepository(session)

    def get_categories(self):
        return self.repository.get_all()

    def create_category(self, name, category_type):
        name = name.strip()

        if not name:
            raise ValueError("Category name is required.")

        if category_type not in ("Income", "Expense"):
            raise ValueError("Category type must be Income or Expense.")

        return self.repository.create_category(
            name=name,
            category_type=category_type,
        )