from app.models.transaction import Transaction
from app.services.transaction_service import TransactionService


class TransactionController:
    """Controller for transaction operations."""

    def __init__(self, session):
        self.service = TransactionService(session)

    def add_transaction(
        self,
        category_id,
        amount,
        description,
        payment_method,
        transaction_date,
        transaction_time,
    ):
        transaction = Transaction(
            category_id=category_id,
            amount=amount,
            description=description,
            payment_method=payment_method,
            transaction_date=transaction_date,
            transaction_time=transaction_time,
        )

        return self.service.add_transaction(transaction)

    def get_transactions(self):
        return self.service.get_transactions()

    def get_today_income(self, today):
        return self.service.get_today_income(today)

    def get_today_expense(self, today):
        return self.service.get_today_expense(today)

    def delete_transaction(self, transaction):
        self.service.delete_transaction(transaction)