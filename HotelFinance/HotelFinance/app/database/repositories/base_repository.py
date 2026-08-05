# Every repository will inherit from this class.

from sqlalchemy.orm import Session


class BaseRepository:
    """Base repository shared by all repositories."""

    def __init__(self, session: Session):
        self.session = session

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj):
        self.session.delete(obj)
        self.session.commit()

    def update(self):
        self.session.commit()