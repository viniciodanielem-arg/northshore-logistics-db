from database.db import get_connection
from utils.logger import log_audit
from utils.security import simple_encrypt


def add_driver(full_name, phone, license_number, license_expiry,
               route_history_notes, shift_assignment, user_id=1):
    if not full_name.strip():
        raise ValueError("Driver name is required.")
    if not license_number.strip():
        raise ValueError("License number is required.")

    conn = get_connection()
    cursor = conn.cursor()

    encrypted_phone = simple_encrypt(phone)
    encrypted_license = simple_encrypt(license_number)

    cursor.execute("""
    INSERT INTO drivers (
        full_name, phone, license_number, license_expiry,
        route_history_notes, shift_assignment
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        full_name,
        encrypted_phone,
        encrypted_license,
        license_expiry,
        route_history_notes,
        shift_assignment
    ))

    driver_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(user_id, "INSERT", "drivers", driver_id, f"Added driver {full_name}")


def get_all_drivers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT driver_id, full_name, phone, license_number, license_expiry, shift_assignment
        FROM drivers
        ORDER BY driver_id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows