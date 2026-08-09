from datetime import date

from app.database.repositories.cash_denomination_repository import CashDenominationRepository


class CashDenominationService:
    """Business logic for daily cash denomination records."""

    def __init__(self, session):
        self.repository = CashDenominationRepository(session)

    def get_by_date(self, denomination_date: date):
        return self.repository.get_by_date(denomination_date)

    def get_or_create(self, denomination_date: date):
        return self.repository.get_or_create(denomination_date)

    def save(self, cash_denomination):
        return self.repository.save(cash_denomination)

    def update(self):
        return self.repository.update()
