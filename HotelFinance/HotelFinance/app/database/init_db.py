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


def create_tables():
    Base.metadata.create_all(bind=engine)
    _ensure_settings_columns()
    print("Database tables created successfully.")
