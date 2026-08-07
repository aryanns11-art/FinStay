from sqlalchemy import create_engine, text

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def close_database_connections():
    """
    Terminate existing connections to the application database.

    This is required before restoring a PostgreSQL database
    that may have active application connections.
    """

    maintenance_url = (
        f"postgresql+psycopg://"
        f"{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/postgres"
    )

    maintenance_engine = create_engine(
        maintenance_url,
        pool_pre_ping=True,
    )

    try:

        with maintenance_engine.connect() as connection:

            connection.execute(
                text(
                    """
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = :database_name
                      AND pid <> pg_backend_pid()
                    """
                ),
                {
                    "database_name": DB_NAME
                },
            )

            connection.commit()

    finally:

        maintenance_engine.dispose()