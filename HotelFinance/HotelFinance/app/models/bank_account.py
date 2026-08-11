"""
Bank account model.

Stores the bank accounts used for Online transactions.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class BankAccount(Base):
    """A bank account used for Online transactions."""

    __tablename__ = "bank_accounts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    account_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    transactions = relationship(
        "Transaction",
        back_populates="bank_account",
        foreign_keys="Transaction.bank_account_id",
    )

    daily_balances = relationship(
        "BankDailyBalance",
        back_populates="bank_account",
        cascade="all, delete-orphan",
    )
