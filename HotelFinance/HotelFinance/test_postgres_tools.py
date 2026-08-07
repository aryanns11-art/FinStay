from app.utils.postgres_tools import PostgreSQLTools


pg_dump = PostgreSQLTools.find_pg_dump()
pg_restore = PostgreSQLTools.find_pg_restore()

print("pg_dump:", pg_dump)
print("pg_restore:", pg_restore)