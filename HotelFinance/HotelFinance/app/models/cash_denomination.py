from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CashDenomination(Base):
    """Stores daily cash denomination counts."""

    __tablename__ = "cash_denominations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    denomination_date: Mapped[date] = mapped_column(
        Date,
        unique=True,
        nullable=False,
    )

    denomination_500: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    denomination_200: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    denomination_100: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    denomination_50: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    denomination_20: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    denomination_10: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    denomination_5: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    denomination_2: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    denomination_1: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
