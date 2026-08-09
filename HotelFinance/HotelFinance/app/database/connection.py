from sqlalchemy import create_engine, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import NullPool

from config import DATABASE_URL, DATA_DIR


DATA_DIR.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False},
    # NullPool ensures dispose() fully releases the SQLite file on Windows.
    poolclass=NullPool,
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable foreign key enforcement for SQLite connections."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def test_connection():
    try:
        with engine.connect():
            print("Connected to SQLite successfully.")
            return True
    except SQLAlchemyError as e:
        print(f"Database Connection Failed:\n{e}")
        return False
