# This file creates tables automatically.

from sqlalchemy import inspect, text

from app.database.base import Base
from app.database.connection import engine

from app.models.business import Business
from app.models.category import Category
from app.models.payment_method import PaymentMethod
from app.models.transaction import Transaction
from app.models.cash_note import CashNote
from app.models.cash_denomination import CashDenomination
from app.models.daily_summary import DailySummary
from app.models.settings import Settings
from app.models.daily_balance import DailyBalance

# New bank-account models — must be imported so SQLAlchemy registers them
from app.models.bank_account import BankAccount          # noqa: F401
from app.models.bank_daily_balance import BankDailyBalance  # noqa: F401


def _ensure_settings_columns():
    """Add hotel-info columns if an older SQLite settings table is missing them."""

    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    if "settings" not in table_names:
        return

    existing = {column["name"] for column in inspector.get_columns("settings")}

    columns_to_add = {
        "hotel_name": "VARCHAR(255)",
        "hotel_address": "VARCHAR(500)",
        "phone_number": "VARCHAR(50)",
        "email": "VARCHAR(255)",
        "gstin": "VARCHAR(50)",
    }

    with engine.begin() as connection:
        for column_name, column_type in columns_to_add.items():
            if column_name not in existing:
                connection.execute(
                    text(
                        f"ALTER TABLE settings ADD COLUMN {column_name} {column_type}"
                    )
                )


def _ensure_transaction_bank_account_column():
    """
    Safely add bank_account_id column to existing transactions table.

    SQLite does not support ALTER TABLE … ADD COLUMN with a FOREIGN KEY
    constraint inline, but it does allow adding a plain nullable column.
    The foreign-key relationship is enforced at the ORM level.
    Existing rows keep NULL which is correct for Cash transactions.
    """
    inspector = inspect(engine)

    if "transactions" not in inspector.get_table_names():
        return  # table will be created fresh by create_all()

    existing = {col["name"] for col in inspector.get_columns("transactions")}

    if "bank_account_id" not in existing:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE transactions ADD COLUMN bank_account_id INTEGER")
            )


def create_tables():
    Base.metadata.create_all(bind=engine)
    _ensure_settings_columns()
    _ensure_transaction_bank_account_column()
    print("Database tables created successfully.")
