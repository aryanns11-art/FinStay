"""
Controller for bank account operations.
Delegates all business logic to BankAccountService.
"""

from datetime import date
from decimal import Decimal

from app.services.bank_account_service import BankAccountService


class BankAccountController:
    """Thin controller that coordinates Flask routes with the service layer."""

    def __init__(self, session):
        self.service = BankAccountService(session)

    # ── Accounts ───────────────────────────────────────────────────────────

    def get_all_accounts(self):
        return self.service.get_all_accounts()

    def get_active_accounts(self):
        return self.service.get_active_accounts()

    def get_account_by_id(self, account_id: int):
        return self.service.get_account_by_id(account_id)

    def create_account(self, name: str, account_number: str | None):
        return self.service.create_account(name, account_number)

    def edit_account(
        self,
        account_id: int,
        name: str,
        account_number: str | None,
    ):
        return self.service.edit_account(account_id, name, account_number)

    def deactivate_account(self, account_id: int):
        return self.service.deactivate_account(account_id)

    # ── Daily balance ──────────────────────────────────────────────────────

    def set_opening_balance(
        self,
        account_id: int,
        balance_date: date,
        opening_balance: Decimal,
    ):
        return self.service.set_opening_balance(
            account_id, balance_date, opening_balance
        )

    def get_opening_balance(self, account_id: int, balance_date: date):
        return self.service.get_opening_balance(account_id, balance_date)

    # ── Summary ────────────────────────────────────────────────────────────

    def get_account_summary(self, account_id: int, today: date) -> dict:
        return self.service.get_account_summary(account_id, today)

    def get_today_transactions(self, account_id: int, today: date):
        return self.service.get_today_transactions(account_id, today)

    def validate_for_online_transaction(self, account_id: int):
        return self.service.validate_for_online_transaction(account_id)

    def has_transactions(self, account_id: int) -> bool:
        return self.service.has_transactions(account_id)
