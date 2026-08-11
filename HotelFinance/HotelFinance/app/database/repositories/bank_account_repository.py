"""
Repository for bank account and bank daily balance operations.
Follows the existing BaseRepository pattern.
"""

from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.database.repositories.base_repository import BaseRepository
from app.models.bank_account import BankAccount
from app.models.bank_daily_balance import BankDailyBalance
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.payment_method import PaymentMethod


class BankAccountRepository(BaseRepository):
    """Repository for bank account operations."""

    # ── Account queries ────────────────────────────────────────────────────

    def get_all(self):
        """Return all bank accounts ordered by name."""
        return (
            self.session.query(BankAccount)
            .order_by(BankAccount.name)
            .all()
        )

    def get_active(self):
        """Return only active bank accounts."""
        return (
            self.session.query(BankAccount)
            .filter(BankAccount.is_active == True)  # noqa: E712
            .order_by(BankAccount.name)
            .all()
        )

    def get_by_id(self, account_id: int):
        """Return a single bank account by primary key."""
        return (
            self.session.query(BankAccount)
            .filter(BankAccount.id == account_id)
            .first()
        )

    def get_by_name(self, name: str):
        """Return a bank account matching the given name (case-insensitive)."""
        return (
            self.session.query(BankAccount)
            .filter(func.lower(BankAccount.name) == name.lower().strip())
            .first()
        )

    # ── Account mutations ──────────────────────────────────────────────────

    def create(self, name: str, account_number: str | None) -> BankAccount:
        """Persist a new bank account and return it."""
        account = BankAccount(
            name=name.strip(),
            account_number=account_number.strip() if account_number else None,
            is_active=True,
        )
        return self.add(account)

    def save_account(self, account: BankAccount) -> BankAccount:
        """Commit an already-modified account object."""
        return self.add(account)

    def deactivate(self, account: BankAccount):
        """Mark account inactive (soft delete)."""
        account.is_active = False
        self.update()

    def hard_delete(self, account: BankAccount):
        """Permanently remove an account with no transactions."""
        self.delete(account)

    # ── Daily balance queries ──────────────────────────────────────────────

    def get_daily_balance(
        self, account_id: int, balance_date: date
    ) -> BankDailyBalance | None:
        """Return the opening-balance record for a specific account + date."""
        return (
            self.session.query(BankDailyBalance)
            .filter(
                BankDailyBalance.bank_account_id == account_id,
                BankDailyBalance.balance_date == balance_date,
            )
            .first()
        )

    # ── Daily balance mutations ────────────────────────────────────────────

    def set_daily_balance(
        self,
        account_id: int,
        balance_date: date,
        opening_balance: Decimal,
    ) -> BankDailyBalance:
        """
        Create or update today's opening balance for an account.
        Never creates a duplicate (account_id, balance_date) record.
        """
        record = self.get_daily_balance(account_id, balance_date)
        if record:
            record.opening_balance = opening_balance
            self.update()
            return record

        record = BankDailyBalance(
            bank_account_id=account_id,
            balance_date=balance_date,
            opening_balance=opening_balance,
        )
        return self.add(record)

    # ── Transaction aggregates for a specific account ──────────────────────

    def _online_payment_method_id(self) -> int | None:
        """Return the primary-key id of the 'Online' payment method."""
        row = (
            self.session.query(PaymentMethod.id)
            .filter(PaymentMethod.name == "Online")
            .first()
        )
        return row[0] if row else None

    def get_today_income(self, account_id: int, today: date) -> Decimal:
        """
        Sum of Online Income transactions for this account today.
        Only transactions assigned to this bank account are counted.
        """
        result = (
            self.session.query(func.sum(Transaction.amount))
            .join(Category, Transaction.category_id == Category.id)
            .join(PaymentMethod, Transaction.payment_method_id == PaymentMethod.id)
            .filter(
                Transaction.bank_account_id == account_id,
                Transaction.transaction_date == today,
                Category.type == "Income",
                PaymentMethod.name == "Online",
            )
            .scalar()
        )
        return Decimal(str(result)) if result else Decimal("0.00")

    def get_today_expense(self, account_id: int, today: date) -> Decimal:
        """
        Sum of Online Expense transactions for this account today.
        """
        result = (
            self.session.query(func.sum(Transaction.amount))
            .join(Category, Transaction.category_id == Category.id)
            .join(PaymentMethod, Transaction.payment_method_id == PaymentMethod.id)
            .filter(
                Transaction.bank_account_id == account_id,
                Transaction.transaction_date == today,
                Category.type == "Expense",
                PaymentMethod.name == "Online",
            )
            .scalar()
        )
        return Decimal(str(result)) if result else Decimal("0.00")

    def get_today_transaction_count(self, account_id: int, today: date) -> int:
        """Count of Online transactions for this account today."""
        return (
            self.session.query(Transaction)
            .join(PaymentMethod, Transaction.payment_method_id == PaymentMethod.id)
            .filter(
                Transaction.bank_account_id == account_id,
                Transaction.transaction_date == today,
                PaymentMethod.name == "Online",
            )
            .count()
        )

    def get_today_transactions(self, account_id: int, today: date):
        """All Online transactions for this account today, newest first."""
        return (
            self.session.query(Transaction)
            .options(
                joinedload(Transaction.category),
                joinedload(Transaction.payment_method),
            )
            .join(PaymentMethod, Transaction.payment_method_id == PaymentMethod.id)
            .filter(
                Transaction.bank_account_id == account_id,
                Transaction.transaction_date == today,
                PaymentMethod.name == "Online",
            )
            .order_by(
                Transaction.transaction_time.desc(),
            )
            .all()
        )

    def has_transactions(self, account_id: int) -> bool:
        """Return True if this account has any associated transactions."""
        return (
            self.session.query(Transaction)
            .filter(Transaction.bank_account_id == account_id)
            .count()
        ) > 0
