from datetime import date

from app.models.cash_denomination import CashDenomination
from app.services.cash_denomination_service import CashDenominationService


class CashDenominationController:
    """Controller for daily cash denomination records."""

    def __init__(self, session):
        self.service = CashDenominationService(session)

    def get_by_date(self, denomination_date: date):
        return self.service.get_by_date(denomination_date)

    def get_or_create(self, denomination_date: date):
        return self.service.get_or_create(denomination_date)

    def save_or_update(self, cash_denomination: CashDenomination):
        if cash_denomination.id is None:
            return self.service.save(cash_denomination)
        return self.service.update()
