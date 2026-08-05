from datetime import date

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CashNote(Base):
    """Stores daily cash note counts."""

    __tablename__ = "cash_notes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    transaction_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    denomination: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )