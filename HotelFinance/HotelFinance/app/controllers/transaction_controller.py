from app.services.transaction_service import TransactionService


class TransactionController:
    """Controller for transaction operations."""

    def __init__(self, session):
        self.service = TransactionService(session)

    def add_transaction(self, transaction):
        """Save a transaction."""
        return self.service.add_transaction(transaction)

    def get_transactions(self):
        return self.service.get_transactions()

    def get_today_income(self, today):
        return self.service.get_today_income(today)

    def get_today_expense(self, today):
        return self.service.get_today_expense(today)

    def delete_transaction(self, transaction):
        self.service.delete_transaction(transaction)

    def search_transactions(self, keyword):
        return self.service.search_transactions(keyword)

    def get_transactions_by_type(self, transaction_type):
        return self.service.get_transactions_by_type(transaction_type)

    def get_cash_income(self, today):
        return self.service.get_cash_income(today)


    def get_cash_expense(self, today):
        return self.service.get_cash_expense(today)


    def get_online_income(self, today):
        return self.service.get_online_income(today)


    def get_online_expense(self, today):
        return self.service.get_online_expense(today)
