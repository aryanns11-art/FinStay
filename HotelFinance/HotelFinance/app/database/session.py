#A Session is your workspace for interacting with the database

from sqlalchemy.orm import sessionmaker

from app.database.connection import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_session():
    """Return a new database session."""
    return SessionLocal()