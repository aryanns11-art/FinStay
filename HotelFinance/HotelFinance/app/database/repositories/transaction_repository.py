from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.database.repositories.base_repository import BaseRepository
from app.models.transaction import Transaction
from app.models.category import Category

from sqlalchemy import cast, String, or_
from sqlalchemy.orm import joinedload
from app.models.payment_method import PaymentMethod

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

    def search(self, keyword: str):
        """Search transactions."""
    
        return (
            self.session.query(Transaction)
            .options(
                joinedload(Transaction.category),
                joinedload(Transaction.payment_method),
            )
            .join(Category)
            .join(PaymentMethod)
            .filter(
                or_(
                    Category.name.ilike(f"%{keyword}%"),
                    PaymentMethod.name.ilike(f"%{keyword}%"),
                    Transaction.description.ilike(f"%{keyword}%"),
                    cast(Transaction.amount, String).ilike(f"%{keyword}%"),
                )
            )
            .order_by(
                Transaction.transaction_date.desc(),
                Transaction.transaction_time.desc(),
            )
            .all()
        )

    def get_by_type(self, transaction_type: str):
        """Return transactions filtered by Income or Expense."""
    
        return (
            self.session.query(Transaction)
            .options(
                joinedload(Transaction.category),
                joinedload(Transaction.payment_method),
            )
            .join(Category)
            .filter(Category.type == transaction_type)
            .order_by(
                Transaction.transaction_date.desc(),
                Transaction.transaction_time.desc(),
            )
            .all()
        )

    def get_cash_income_total(self, transaction_date: date):
        result = (
            self.session.query(func.sum(Transaction.amount))
            .join(Category)
            .join(Transaction.payment_method)
            .filter(
                Transaction.transaction_date == transaction_date,
                Category.type == "Income",
                PaymentMethod.name == "Cash",
            )
            .scalar()
        )

        return result or Decimal("0.00")

    def get_cash_expense_total(self, transaction_date: date):
        result = (
            self.session.query(func.sum(Transaction.amount))
            .join(Category)
            .join(Transaction.payment_method)
            .filter(
                Transaction.transaction_date == transaction_date,
                Category.type == "Expense",
                PaymentMethod.name == "Cash",
            )
            .scalar()
        )

        return result or Decimal("0.00")

    def get_online_income_total(self, transaction_date: date):
        result = (
            self.session.query(func.sum(Transaction.amount))
            .join(Category)
            .join(Transaction.payment_method)
            .filter(
                Transaction.transaction_date == transaction_date,
                Category.type == "Income",
                PaymentMethod.name == "Online",
            )
            .scalar()
        )

        return result or Decimal("0.00")

    def get_online_expense_total(self, transaction_date: date):
        result = (
            self.session.query(func.sum(Transaction.amount))
            .join(Category)
            .join(Transaction.payment_method)
            .filter(
                Transaction.transaction_date == transaction_date,
                Category.type == "Expense",
                PaymentMethod.name == "Online",
            )
            .scalar()
        )

        return result or Decimal("0.00")
