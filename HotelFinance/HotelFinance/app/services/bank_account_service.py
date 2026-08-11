"""
Business logic for bank accounts.
All monetary values use Decimal — no float arithmetic.
"""

from datetime import date
from decimal import Decimal

from app.database.repositories.bank_account_repository import BankAccountRepository
from app.models.bank_account import BankAccount


class BankAccountService:
    """Service layer for bank account operations."""

    def __init__(self, session):
        self.repository = BankAccountRepository(session)

    # ── Account management ─────────────────────────────────────────────────

    def get_all_accounts(self):
        """Return every bank account (active and inactive)."""
        return self.repository.get_all()

    def get_active_accounts(self):
        """Return only active bank accounts (for dropdown lists)."""
        return self.repository.get_active()

    def get_account_by_id(self, account_id: int):
        """Return a single account or None."""
        return self.repository.get_by_id(account_id)

    def create_account(self, name: str, account_number: str | None) -> BankAccount:
        """
        Create a new bank account.
        Raises ValueError if name is blank or already taken.
        """
        name = (name or "").strip()
        if not name:
            raise ValueError("Account name is required.")

        existing = self.repository.get_by_name(name)
        if existing:
            raise ValueError(f"A bank account named '{name}' already exists.")

        return self.repository.create(name, account_number)

    def edit_account(
        self,
        account_id: int,
        name: str,
        account_number: str | None,
    ) -> BankAccount:
        """
        Update an existing account's name and/or account number.
        Raises ValueError for invalid input or duplicate name.
        """
        name = (name or "").strip()
        if not name:
            raise ValueError("Account name is required.")

        account = self.repository.get_by_id(account_id)
        if not account:
            raise ValueError("Bank account not found.")

        # Allow keeping the same name; only block a different account using it
        duplicate = self.repository.get_by_name(name)
        if duplicate and duplicate.id != account_id:
            raise ValueError(f"A bank account named '{name}' already exists.")

        account.name = name
        account.account_number = account_number.strip() if account_number else None
        self.repository.update()
        return account

    def deactivate_account(self, account_id: int):
        """
        Deactivate an account.  Historical transactions are preserved.
        If the account has no transactions it may be hard-deleted instead —
        but we always prefer deactivation for safety.
        """
        account = self.repository.get_by_id(account_id)
        if not account:
            raise ValueError("Bank account not found.")
        if not account.is_active:
            raise ValueError("Bank account is already inactive.")

        self.repository.deactivate(account)

    # ── Daily opening balance ──────────────────────────────────────────────

    def set_opening_balance(
        self,
        account_id: int,
        balance_date: date,
        opening_balance: Decimal,
    ):
        """
        Create or update today's opening balance for an account.
        Never duplicates records — updates in place if one already exists.
        """
        if opening_balance < Decimal("0.00"):
            raise ValueError("Opening balance cannot be negative.")

        account = self.repository.get_by_id(account_id)
        if not account:
            raise ValueError("Bank account not found.")

        return self.repository.set_daily_balance(
            account_id, balance_date, opening_balance
        )

    def get_opening_balance(self, account_id: int, balance_date: date):
        """Return the daily balance record for an account on a given date, or None."""
        return self.repository.get_daily_balance(account_id, balance_date)

    # ── Today's summary ────────────────────────────────────────────────────

    def get_account_summary(self, account_id: int, today: date) -> dict:
        """
        Return a dict with today's financial summary for a bank account:
        {
            opening_balance:    Decimal or None,
            income:             Decimal,
            expense:            Decimal,
            current_balance:    Decimal or None,
            transaction_count:  int,
            has_opening_balance: bool,
        }
        current_balance is None when no opening balance is set for today.
        """
        balance_record = self.repository.get_daily_balance(account_id, today)
        opening = (
            Decimal(str(balance_record.opening_balance))
            if balance_record
            else None
        )

        income = self.repository.get_today_income(account_id, today)
        expense = self.repository.get_today_expense(account_id, today)
        count = self.repository.get_today_transaction_count(account_id, today)

        current_balance = (
            opening + income - expense
            if opening is not None
            else None
        )

        return {
            "opening_balance": opening,
            "income": income,
            "expense": expense,
            "current_balance": current_balance,
            "transaction_count": count,
            "has_opening_balance": opening is not None,
        }

    def get_today_transactions(self, account_id: int, today: date):
        """Return all Online transactions for this account today."""
        return self.repository.get_today_transactions(account_id, today)

    def validate_for_online_transaction(self, account_id: int) -> BankAccount:
        """
        Validate that the given account_id is valid and active.
        Raises ValueError with a user-friendly message if not.
        Used by transaction routes for server-side validation.
        """
        if not account_id:
            raise ValueError("Online transactions require a bank account.")

        account = self.repository.get_by_id(account_id)
        if not account:
            raise ValueError("Selected bank account is not available.")
        if not account.is_active:
            raise ValueError("Selected bank account is not available.")

        return account

    def has_transactions(self, account_id: int) -> bool:
        """Check if an account has any transaction history."""
        return self.repository.has_transactions(account_id)
