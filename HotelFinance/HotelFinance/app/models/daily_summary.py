from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class DailySummary(Base):
    """Stores end-of-day cash summary."""

    __tablename__ = "daily_summary"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    summary_date: Mapped[date] = mapped_column(
        Date,
        unique=True,
        nullable=False,
    )

    opening_cash: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    closing_cash: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    expected_cash: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    actual_cash: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )