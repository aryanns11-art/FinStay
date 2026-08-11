"""
Bank daily balance model.

One opening-balance record per bank account per calendar date.
"""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class BankDailyBalance(Base):
    """Daily opening balance for a specific bank account."""

    __tablename__ = "bank_daily_balances"

    # Enforce one record per (account, date)
    __table_args__ = (
        UniqueConstraint(
            "bank_account_id",
            "balance_date",
            name="uq_bank_daily_balance",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    bank_account_id: Mapped[int] = mapped_column(
        ForeignKey("bank_accounts.id"),
        nullable=False,
    )

    balance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    opening_balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    bank_account = relationship(
        "BankAccount",
        back_populates="daily_balances",
    )
