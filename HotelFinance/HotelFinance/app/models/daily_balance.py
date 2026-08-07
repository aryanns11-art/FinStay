from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class DailyBalance(Base):
    """Stores daily opening balances."""

    __tablename__ = "daily_balances"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    balance_date: Mapped[date] = mapped_column(
        Date,
        unique=True,
        nullable=False,
    )

    cash_opening: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    online_opening: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )