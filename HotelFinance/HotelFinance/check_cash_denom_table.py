from app.database.connection import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='cash_denominations';"))
    print('table_exists', result.scalar() is not None)
    info = conn.execute(text("PRAGMA table_info('cash_denominations');")).fetchall()
    print(info)
