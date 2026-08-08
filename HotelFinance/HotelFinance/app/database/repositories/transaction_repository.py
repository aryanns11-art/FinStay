from datetime import date
from decimal import Decimal

from sqlalchemy import case, cast, func, or_, String
from sqlalchemy.orm import joinedload

from app.database.repositories.base_repository import BaseRepository
from app.models.transaction import Transaction
from app.models.category import Category
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

    def get_income_transaction_count(self, transaction_date: date):
        """Return today's income transaction count."""

        return (
            self.session.query(Transaction)
            .join(Category)
            .filter(
                Transaction.transaction_date == transaction_date,
                Category.type == "Income",
            )
            .count()
        )

    def get_expense_transaction_count(self, transaction_date: date):
        """Return today's expense transaction count."""

        return (
            self.session.query(Transaction)
            .join(Category)
            .filter(
                Transaction.transaction_date == transaction_date,
                Category.type == "Expense",
            )
            .count()
        )

    def get_highest_income_transaction(self, transaction_date: date):
        """Return today's highest income transaction."""
    
        return (
            self.session.query(Transaction)
            .join(Category)
            .filter(
                Transaction.transaction_date == transaction_date,
                Category.type == "Income",
            )
            .order_by(Transaction.amount.desc())
            .first()
        )
    
    def get_highest_expense_transaction(self, transaction_date: date):
        """Return today's highest expense transaction."""
    
        return (
            self.session.query(Transaction)
            .join(Category)
            .filter(
                Transaction.transaction_date == transaction_date,
                Category.type == "Expense",
            )
            .order_by(Transaction.amount.desc())
            .first()
        )


    def get_monthly_income(self, month: int, year: int):
        result = (
            self.session.query(func.sum(Transaction.amount))
            .join(Category)
            .filter(
                func.extract("month", Transaction.transaction_date) == month,
                func.extract("year", Transaction.transaction_date) == year,
                Category.type == "Income",
            )
            .scalar()
        )

        return result or Decimal("0.00")

    def get_monthly_expense(self, month: int, year: int):
        result = (
            self.session.query(func.sum(Transaction.amount))
            .join(Category)
            .filter(
                func.extract("month", Transaction.transaction_date) == month,
                func.extract("year", Transaction.transaction_date) == year,
                Category.type == "Expense",
            )
            .scalar()
        )

        return result or Decimal("0.00")

    def get_monthly_transaction_count(self, month: int, year: int):
        return (
            self.session.query(Transaction)
            .filter(
                func.extract("month", Transaction.transaction_date) == month,
                func.extract("year", Transaction.transaction_date) == year,
            )
            .count()
        )

    def get_income_by_category(self,month: int,year: int):
        return (
            self.session.query(
                Category.name,
                func.sum(Transaction.amount),
            )
            .join(Category)
            .filter(
                func.extract(
                    "month",
                    Transaction.transaction_date,
                )
                == month,
                func.extract(
                    "year",
                    Transaction.transaction_date,
                )
                == year,
                Category.type == "Income",
            )
            .group_by(Category.name)
            .order_by(
                func.sum(Transaction.amount).desc()
            )
            .all()
        )


    def get_expense_by_category(self,month: int,year: int):
        return (
            self.session.query(
                Category.name,
                func.sum(Transaction.amount),
            )
            .join(Category)
            .filter(
                func.extract(
                    "month",
                    Transaction.transaction_date,
                )
                == month,
                func.extract(
                    "year",
                    Transaction.transaction_date,
                )
                == year,
                Category.type == "Expense",
            )
            .group_by(Category.name)
            .order_by(
                func.sum(Transaction.amount).desc()
            )
            .all()
        )

    def get_daily_income_expense(self, month: int, year: int):
        return (
            self.session.query(
                cast(func.extract("day", Transaction.transaction_date), String).label("day"),
                func.coalesce(
                    func.sum(
                        case(
                            (Category.type == "Income", Transaction.amount),
                            else_=0,
                        )
                    ),
                    0,
                ).label("income"),
                func.coalesce(
                    func.sum(
                        case(
                            (Category.type == "Expense", Transaction.amount),
                            else_=0,
                        )
                    ),
                    0,
                ).label("expense"),
            )
            .join(Category)
            .filter(
                func.extract("month", Transaction.transaction_date) == month,
                func.extract("year", Transaction.transaction_date) == year,
            )
            .group_by("day")
            .order_by("day")
            .all()
        )

    def get_today_cash_income(self, today):
        result = (
            self.session.query(
                func.sum(Transaction.amount)
            )
            .join(Category)
            .join(Transaction.payment_method)
            .filter(
                Transaction.transaction_date == today,
                Category.type == "Income",
                Transaction.payment_method.has(
                    name="Cash"
                ),
            )
            .scalar()
        )

        return result or Decimal("0.00")

    def get_today_cash_expense(self, today):
        result = (
            self.session.query(
                func.sum(Transaction.amount)
            )
            .join(Category)
            .join(Transaction.payment_method)
            .filter(
                Transaction.transaction_date == today,
                Category.type == "Expense",
                Transaction.payment_method.has(
                    name="Cash"
                ),
            )
            .scalar()
        )

        return result or Decimal("0.00")


    def get_today_cash_transactions(self,today):
        return (
            self.session.query(Transaction)
            .join(Transaction.payment_method)
            .filter(
                Transaction.transaction_date == today,
                Transaction.payment_method.has(
                    name="Cash"
                ),
            )
            .order_by(
                Transaction.transaction_time.desc()
            )
            .all()
        )

    def _get_total(self, today, payment_name, category_type):

        total = (
            self.session.query(
                func.coalesce(
                    func.sum(Transaction.amount),
                    0,
                )
            )
            .join(Category)
            .join(PaymentMethod)
            .filter(
                Transaction.transaction_date == today,
                Category.type == category_type,
                PaymentMethod.name == payment_name,
            )
            .scalar()
        )

        return total

    def get_today_cash_income(self, today):
        return self._get_total(
            today,
            "Cash",
            "Income",
        )


    def get_today_cash_expense(self, today):
        return self._get_total(
            today,
            "Cash",
            "Expense",
        )


    def get_today_online_income(self, today):
        return self._get_total(
            today,
            "Online",
            "Income",
        )


    def get_today_online_expense(self, today):
        return self._get_total(
            today,
            "Online",
            "Expense",
        )
    
    def get_today_transactions(self, today):

        return (
            self.session.query(Transaction)
            .filter(
                Transaction.transaction_date == today
            )
            .order_by(
                Transaction.transaction_time.desc()
            )
            .all()
        )