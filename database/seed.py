from database.db import get_connection
from utils.security import generate_salt, hash_password


def seed_roles():
    conn = get_connection()
    cursor = conn.cursor()

    roles = [("admin",), ("manager",), ("warehouse_staff",), ("driver",)]

    cursor.executemany("""
        INSERT OR IGNORE INTO roles (role_name)
        VALUES (?)
    """, roles)

    conn.commit()
    conn.close()


def seed_admin_user():
    conn = get_connection()
    cursor = conn.cursor()

    salt = generate_salt()
    password_hash = hash_password("admin123", salt)

    cursor.execute("""
        INSERT OR IGNORE INTO users (
            user_id, username, password_hash, salt, role_id, full_name, email, is_active
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        1,
        "admin",
        password_hash,
        salt,
        1,
        "System Admin",
        "admin@northshore.local",
        1
    ))

    conn.commit()
    conn.close()