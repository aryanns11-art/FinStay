from datetime import date

from app.database.repositories.base_repository import BaseRepository
from app.models.cash_note import CashNote


class CashNoteRepository(BaseRepository):
    """Repository for daily cash note counts."""

    def get_by_date(self, transaction_date: date):
        return (
            self.session.query(CashNote)
            .filter(
                CashNote.transaction_date == transaction_date
            )
            .all()
        )