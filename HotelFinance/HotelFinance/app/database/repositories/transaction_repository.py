from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import joinedload


from app.database.repositories.base_repository import BaseRepository
from app.models.transaction import Transaction
from app.models.category import Category


class TransactionRepository(BaseRepository):
    """Repository for transaction-related database operations."""

    def get_all(self):

        self.session.expire_all()
        return (
            self.session.query(Transaction)
            .options(
                joinedload(Transaction.category),
                joinedload(Transaction.payment_method),
            )
            .order_by(
                Transaction.transaction_date.desc(),
                Transaction.transaction_time.desc(),
            )
            .all()
        )

    def get_by_id(self, transaction_id: int):
        return (
            self.session.query(Transaction)
            .filter(Transaction.id == transaction_id)
            .first()
        )

    def get_by_date(self, transaction_date: date):
        return (
            self.session.query(Transaction)
            .filter(Transaction.transaction_date == transaction_date)
            .all()
        )

    def get_income_total(self, transaction_date: date):
        result = (
            self.session.query(func.sum(Transaction.amount))
            .join(Category)
            .filter(
                Transaction.transaction_date == transaction_date,
                Category.type == "Income",
            )
            .scalar()
        )

        return result or Decimal("0.00")

    def get_expense_total(self, transaction_date: date):
        result = (
            self.session.query(func.sum(Transaction.amount))
            .join(Category)
            .filter(
                Transaction.transaction_date == transaction_date,
                Category.type == "Expense",
            )
            .scalar()
        )

        return result or Decimal("0.00")