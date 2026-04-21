from database.db import get_connection
from utils.logger import log_audit

def update_vehicle(vehicle_id, vehicle_type, capacity, maintenance_due_date,
                   availability_status, assigned_warehouse_id, user_id=1):
    if not str(vehicle_id).strip():
        raise ValueError("Vehicle ID is required.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT vehicle_id FROM vehicles WHERE vehicle_id = ?", (vehicle_id,))
    existing = cursor.fetchone()

    if not existing:
        conn.close()
        raise ValueError(f"Vehicle ID {vehicle_id} does not exist.")

    cursor.execute("""
        UPDATE vehicles
        SET vehicle_type = ?,
            capacity = ?,
            maintenance_due_date = ?,
            availability_status = ?,
            assigned_warehouse_id = ?
        WHERE vehicle_id = ?
    """, (
        vehicle_type,
        capacity,
        maintenance_due_date,
        availability_status,
        assigned_warehouse_id,
        vehicle_id
    ))

    conn.commit()
    conn.close()

    log_audit(
        user_id,
        "UPDATE",
        "vehicles",
        vehicle_id,
        f"Updated vehicle {vehicle_id}"
    )

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