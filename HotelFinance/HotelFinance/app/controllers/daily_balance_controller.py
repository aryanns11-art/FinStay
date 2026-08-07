from app.models.daily_balance import DailyBalance
from app.services.daily_balance_service import (DailyBalanceService,)


class DailyBalanceController:
    """Controller for daily balances."""

    def __init__(self, session):
        self.service = DailyBalanceService(session)

    def get_balance(self, balance_date):
        return self.service.get_balance(balance_date)

    def create_balance(self,balance_date,cash_opening,online_opening):
        balance = DailyBalance(
            balance_date=balance_date,
            cash_opening=cash_opening,
            online_opening=online_opening,
        )

        return self.service.save_balance(balance)

    def update_balance(self):
        self.service.update_balance()