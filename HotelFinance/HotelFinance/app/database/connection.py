from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from config import (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD,)

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
)


def test_connection():
    try:
        with engine.connect():
            print("✅ Connected to PostgreSQL successfully.")
            return True
    except SQLAlchemyError as e:
        print(f"❌ Database Connection Failed:\n{e}")
        return False