from app.database.connection import test_connection
from app.database.init_db import create_tables


def main():
    if test_connection():
        create_tables()


if __name__ == "__main__":
    main()