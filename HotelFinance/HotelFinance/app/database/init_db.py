#This file creates tables automatically.

from app.database.base import Base
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
    print("✅ Database tables created successfully.")