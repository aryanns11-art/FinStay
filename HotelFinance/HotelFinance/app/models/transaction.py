#This file defines our first database table.

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Time,)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Transaction(Base):
    """Stores every income and expense transaction."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
    )

    payment_method_id: Mapped[int] = mapped_column(
        ForeignKey("payment_methods.id"),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    transaction_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    transaction_time: Mapped[datetime] = mapped_column(
        Time,
        default=datetime.now,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    category = relationship(
        "Category",
        back_populates="transactions",
    )

    payment_method = relationship(
        "PaymentMethod",
        back_populates="transactions",
    )