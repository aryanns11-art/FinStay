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
    

    def get_income_transaction_count(self, today):
        return self.repository.get_income_transaction_count(today)

    def get_expense_transaction_count(self, today):
        return self.repository.get_expense_transaction_count(today)


    def get_highest_income_transaction(self, today):
        return self.repository.get_highest_income_transaction(today)

    def get_highest_expense_transaction(self, today):
        return self.repository.get_highest_expense_transaction(today)

    def get_monthly_income(self, month, year):
        return self.repository.get_monthly_income(month, year)


    def get_monthly_expense(self, month, year):
        return self.repository.get_monthly_expense(month, year)


    def get_monthly_transaction_count(self, month, year):
        return self.repository.get_monthly_transaction_count(month,year)

    def get_income_by_category(self,month,year):
        return self.repository.get_income_by_category(month,year)

    def get_expense_by_category(self,month,year):
        return self.repository.get_expense_by_category(month,year)


    def get_today_cash_income(self, today):
        return self.repository.get_today_cash_income(today)


    def get_today_cash_expense(self, today):
        return self.repository.get_today_cash_expense(today)


    def get_today_online_income(self, today):
        return self.repository.get_today_online_income(today)


    def get_today_online_expense(self, today):
        return self.repository.get_today_online_expense(today)


    def get_today_transactions(self, today):
        return self.repository.get_today_transactions(today)
