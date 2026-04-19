from database.db import get_connection
from utils.logger import log_audit


def add_vehicle(registration_number, vehicle_type, capacity,
                maintenance_due_date, availability_status,
                assigned_warehouse_id, user_id=1):
    if not registration_number.strip():
        raise ValueError("Registration number is required.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vehicles (
            registration_number, vehicle_type, capacity,
            maintenance_due_date, availability_status, assigned_warehouse_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        registration_number,
        vehicle_type,
        capacity,
        maintenance_due_date,
        availability_status,
        assigned_warehouse_id
    ))

    vehicle_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(user_id, "INSERT", "vehicles", vehicle_id, f"Added vehicle {registration_number}")


def get_all_vehicles():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT vehicle_id, registration_number, vehicle_type, capacity,
               maintenance_due_date, availability_status, assigned_warehouse_id
        FROM vehicles
        ORDER BY vehicle_id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows