# Every repository will inherit from this class.

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.utils.logger import logger


class BaseRepository:
    """Base repository shared by all repositories."""

    def __init__(self, session: Session):
        self.session = session

    def add(self, obj):
        try:
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)
            return obj
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception("Database error while saving a record.")
            raise

    def delete(self, obj):
        try:
            self.session.delete(obj)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception("Database error while deleting a record.")
            raise

    def update(self):
        try:
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception("Database error while updating a record.")
            raise
