from database.db import get_connection
from utils.security import generate_salt, hash_password


def seed_roles():
    conn = get_connection()
    cursor = conn.cursor()

    roles = [
        ("admin",),
        ("manager",),
        ("warehouse_staff",),
        ("driver",)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO roles (role_name)
        VALUES (?)
    """, roles)

    conn.commit()
    conn.close()


def seed_admin_user():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE username = ?", ("admin",))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return

    cursor.execute("SELECT role_id FROM roles WHERE role_name = ?", ("admin",))
    role = cursor.fetchone()

    if not role:
        conn.close()
        raise ValueError("Admin role does not exist. Run seed_roles() first.")

    role_id = role[0]

    salt = generate_salt()
    password_hash = hash_password("admin123", salt)

    cursor.execute("""
        INSERT INTO users (
            username, password_hash, salt, role_id, full_name, email, is_active
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "admin",
        password_hash,
        salt,
        role_id,
        "System Admin",
        "admin@northshore.local",
        1
    ))

    conn.commit()
    conn.close()