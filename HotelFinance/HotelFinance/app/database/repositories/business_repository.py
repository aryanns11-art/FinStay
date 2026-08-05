from app.database.repositories.base_repository import BaseRepository
from app.models.business import Business


class BusinessRepository(BaseRepository):

    def get_business(self):
        return self.session.query(Business).first()

    def exists(self):
        return self.get_business() is not None