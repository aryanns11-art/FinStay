from app.database.repositories.daily_balance_repository import (DailyBalanceRepository)


class DailyBalanceService:
    """Business logic for daily balances."""

    def __init__(self, session):
        self.repository = DailyBalanceRepository(session)

    def get_balance(self, balance_date):
        return self.repository.get_by_date(balance_date)

    def save_balance(self, balance):
        return self.repository.save(balance)

    def update_balance(self):
        self.repository.update()