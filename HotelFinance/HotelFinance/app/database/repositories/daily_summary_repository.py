from datetime import date

from app.database.repositories.base_repository import BaseRepository
from app.models.daily_summary import DailySummary


class DailySummaryRepository(BaseRepository):
    """Repository for daily summaries."""

    def get_by_date(self, summary_date: date):
        return (
            self.session.query(DailySummary)
            .filter(
                DailySummary.summary_date == summary_date
            )
            .first()
        )