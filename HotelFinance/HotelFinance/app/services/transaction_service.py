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