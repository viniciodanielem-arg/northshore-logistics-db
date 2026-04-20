from database.schema import create_tables
from database.seed import seed_roles, seed_admin_user

create_tables()
seed_roles()
seed_admin_user()

print("Database, tables, and starter data created successfully.")