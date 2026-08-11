from app.database.repositories.base_repository import BaseRepository
from app.models.category import Category
from app.models.transaction import Transaction


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
            .order_by(Category.name)
            .all()
        )

    def get_expense_categories(self):
        return (
            self.session.query(Category)
            .filter(Category.type == "Expense")
            .order_by(Category.name)
            .all()
        )

    def create_category(self, name, category_type):
        category = Category(
            name=name,
            type=category_type,
            is_default=False,
        )

        return self.add(category)

    def delete_category(self, category_id):
        category = (
            self.session.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

        if not category:
            raise ValueError("Category not found.")

        transaction_exists = (
            self.session.query(Transaction.id)
            .filter(Transaction.category_id == category_id)
            .first()
            is not None
        )

        if transaction_exists:
            raise ValueError(
                "This category cannot be deleted because it is used by existing transactions."
            )

        self.delete(category)
        self.session.commit()

        return True