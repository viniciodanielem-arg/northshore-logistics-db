from database.schema import create_tables
from database.seed import seed_roles

create_tables()
seed_roles()

print("Database, tables, and starter data created successfully.")