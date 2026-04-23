from database.schema import create_tables
from database.seed import seed_roles, seed_admin_user
from ui.app import open_login_window

create_tables()
seed_roles()
seed_admin_user()
open_login_window()