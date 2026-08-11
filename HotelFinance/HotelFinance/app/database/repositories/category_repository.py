from app.database.repositories.base_repository import BaseRepository
from app.models.category import Category


class CategoryRepository(BaseRepository):

    def get_all(self):
        return (
            self.session.query(Category)
            .order_by(Category.name)
            .all()
        )

    def get_income_categories(self):
        return (
            self.session.query(Category)
            .filter(Category.type == "Income")
            .all()
        )

    def get_expense_categories(self):
        return (
            self.session.query(Category)
            .filter(Category.type == "Expense")
            .all()
        )

    def create_category(self, name, category_type):
        category = Category(
            name=name,
            type=category_type,
            is_default=False,
        )

        return self.add(category)