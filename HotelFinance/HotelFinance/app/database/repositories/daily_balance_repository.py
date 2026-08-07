from datetime import date

from app.database.repositories.base_repository import BaseRepository
from app.models.daily_balance import DailyBalance


class DailyBalanceRepository(BaseRepository):
    """Repository for daily opening balances."""

    def get_by_date(self, balance_date: date):
        return (
            self.session.query(DailyBalance)
            .filter(
                DailyBalance.balance_date == balance_date
            )
            .first()
        )

    def save(self, daily_balance):
        return self.add(daily_balance)

    def update(self):
        self.session.commit()