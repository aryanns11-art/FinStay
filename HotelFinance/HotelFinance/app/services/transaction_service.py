from ast import keyword
from decimal import Decimal

from app.database.repositories.transaction_repository import TransactionRepository


class TransactionService:
    """Business logic for transactions."""

    def __init__(self, session):
        self.repository = TransactionRepository(session)

    def add_transaction(self, transaction):
        if transaction.amount <= Decimal("0.00"):
            raise ValueError("Amount must be greater than zero.")

        return self.repository.add(transaction)

    def delete_transaction(self, transaction):
        self.repository.delete(transaction)

    def get_transactions(self):
        return self.repository.get_all()

    def get_today_income(self, today):
        return self.repository.get_income_total(today)

    def get_today_expense(self, today):
        return self.repository.get_expense_total(today)

    def search_transactions(self, keyword):
        return self.repository.search(keyword)

    def get_transactions_by_type(self, transaction_type):
        return self.repository.get_by_type(transaction_type)

    def get_cash_income(self, today):
        return self.repository.get_cash_income_total(today)


    def get_cash_expense(self, today):
        return self.repository.get_cash_expense_total(today)


    def get_online_income(self, today):
        return self.repository.get_online_income_total(today)


    def get_online_expense(self, today):
        return self.repository.get_online_expense_total(today)
