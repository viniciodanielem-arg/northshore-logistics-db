from database.db import get_connection
from utils.logger import log_audit
from utils.validation import (
    validate_required,
    validate_positive_number,
    validate_choice,
    validate_date,
    validate_record_exists,
    ALLOWED_VEHICLE_STATUSES
)


def add_vehicle(registration_number, vehicle_type, capacity,
                maintenance_due_date, availability_status,
                assigned_warehouse_id, user_id=1):

    validate_required(registration_number, "Registration number")
    validate_required(vehicle_type, "Vehicle type")
    validate_positive_number(capacity, "Capacity")
    validate_date(maintenance_due_date, "Maintenance due date")
    validate_choice(availability_status, "Vehicle status", ALLOWED_VEHICLE_STATUSES)
    validate_record_exists("warehouses", "warehouse_id", assigned_warehouse_id, "Warehouse ID")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT vehicle_id FROM vehicles WHERE registration_number = ?", (registration_number,))
    if cursor.fetchone():
        conn.close()
        raise ValueError("Registration number already exists.")

    cursor.execute("""
        INSERT INTO vehicles (
            registration_number, vehicle_type, capacity,
            maintenance_due_date, availability_status, assigned_warehouse_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        registration_number.strip(),
        vehicle_type.strip(),
        float(capacity),
        maintenance_due_date,
        availability_status,
        assigned_warehouse_id
    ))

    vehicle_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(user_id, "INSERT", "vehicles", vehicle_id, f"Added vehicle {registration_number}")

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