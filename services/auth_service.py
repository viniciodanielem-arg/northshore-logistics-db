from database.db import get_connection
from utils.security import generate_salt, hash_password, verify_password
from utils.logger import log_audit


def get_role_id(role_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT role_id FROM roles WHERE role_name = ?", (role_name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]
    return None


def register_user(username, password, role_name, full_name, email, user_id=None):
    if not username.strip():
        raise ValueError("Username is required.")
    if not password.strip():
        raise ValueError("Password is required.")
    if not role_name.strip():
        raise ValueError("Role is required.")
    if not full_name.strip():
        raise ValueError("Full name is required.")

    role_id = get_role_id(role_name)
    if role_id is None:
        raise ValueError(f"Role '{role_name}' does not exist.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        raise ValueError("Username already exists.")

    salt = generate_salt()
    password_hash = hash_password(password, salt)

    cursor.execute("""
        INSERT INTO users (username, password_hash, salt, role_id, full_name, email, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (username, password_hash, salt, role_id, full_name, email, 1))

    new_user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(user_id, "INSERT", "users", new_user_id, f"Registered user {username}")


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.user_id, u.username, u.password_hash, u.salt, u.full_name, u.is_active, r.role_name
        FROM users u
        JOIN roles r ON u.role_id = r.role_id
        WHERE u.username = ?
    """, (username,))

    user = cursor.fetchone()
    conn.close()

    if not user:
        raise ValueError("Invalid username or password.")

    user_id, db_username, password_hash, salt, full_name, is_active, role_name = user

    if is_active != 1:
        raise ValueError("This account is inactive.")

    if not verify_password(password, salt, password_hash):
        raise ValueError("Invalid username or password.")

    return {
        "user_id": user_id,
        "username": db_username,
        "full_name": full_name,
        "role_name": role_name
    }


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.user_id, u.username, u.full_name, u.email, r.role_name, u.is_active
        FROM users u
        JOIN roles r ON u.role_id = r.role_id
        ORDER BY u.user_id
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows