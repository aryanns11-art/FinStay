from app.database.repositories.base_repository import BaseRepository
from app.models.payment_method import PaymentMethod


class PaymentMethodRepository(BaseRepository):

    def get_all(self):
        return (
            self.session.query(PaymentMethod)
            .filter(PaymentMethod.is_active == True)
            .order_by(PaymentMethod.name)
            .all()
        )