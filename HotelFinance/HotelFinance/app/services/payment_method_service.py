from app.database.repositories.payment_method_repository import (
    PaymentMethodRepository,
)


class PaymentMethodService:
    """Business logic for payment methods."""

    def __init__(self, session):
        self.repository = PaymentMethodRepository(session)

    def get_payment_methods(self):
        return self.repository.get_all()