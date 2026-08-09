from datetime import date

from app.database.repositories.base_repository import BaseRepository
from app.models.cash_denomination import CashDenomination


class CashDenominationRepository(BaseRepository):
    """Repository for daily cash denomination records."""

    def get_by_date(self, denomination_date: date):
        return (
            self.session.query(CashDenomination)
            .filter(CashDenomination.denomination_date == denomination_date)
            .first()
        )

    def get_or_create(self, denomination_date: date):
        record = self.get_by_date(denomination_date)
        if record:
            return record

        record = CashDenomination(denomination_date=denomination_date)
        return self.add(record)

    def save(self, cash_denomination):
        return self.add(cash_denomination)

    def update(self):
        return super().update()
