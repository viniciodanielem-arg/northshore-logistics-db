from database.db import get_connection

def seed_roles():
    conn = get_connection()
    cursor = conn.cursor()

    roles = [("admin",), ("manager",), ("warehouse_staff",), ("driver,",)]

    cursor.executemany("""
        INSERT OR IGNORE INTO roles (role_name)
        VALUES (?)
    """, roles)

    conn.commit()
    conn.close()