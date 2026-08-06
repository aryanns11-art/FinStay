from app.services.payment_method_service import PaymentMethodService


class PaymentMethodController:
    """Controller for payment method operations."""

    def __init__(self, session):
        self.service = PaymentMethodService(session)

    def get_payment_methods(self):
        """Return all payment methods."""
        return self.service.get_payment_methods()