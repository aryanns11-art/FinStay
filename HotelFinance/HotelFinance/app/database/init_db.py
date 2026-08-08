#This file creates tables automatically.

from app.database.base import Base
from sqlalchemy import text

from app.database.connection import engine

from app.models.business import Business
from app.models.category import Category
from app.models.payment_method import PaymentMethod
from app.models.transaction import Transaction
from app.models.cash_note import CashNote
from app.models.daily_summary import DailySummary
from app.models.settings import Settings
from app.models.daily_balance import DailyBalance


def create_tables():
    Base.metadata.create_all(bind=engine)

    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE settings ADD COLUMN IF NOT EXISTS hotel_name VARCHAR(255)"))
        connection.execute(text("ALTER TABLE settings ADD COLUMN IF NOT EXISTS hotel_address VARCHAR(500)"))
        connection.execute(text("ALTER TABLE settings ADD COLUMN IF NOT EXISTS phone_number VARCHAR(50)"))
        connection.execute(text("ALTER TABLE settings ADD COLUMN IF NOT EXISTS email VARCHAR(255)"))
        connection.execute(text("ALTER TABLE settings ADD COLUMN IF NOT EXISTS gstin VARCHAR(50)"))
    print("✅ Database tables created successfully.")
