from database.db import get_connection
from utils.logger import log_audit

def update_delivery_assignment(assignment_id, driver_id, vehicle_id, route_details,
                               delivery_date, dispatch_time, arrival_time,
                               assignment_status, user_id=1):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT assignment_id
        FROM delivery_assignments
        WHERE assignment_id = ?
    """, (assignment_id,))
    existing = cursor.fetchone()

    if not existing:
        conn.close()
        raise ValueError(f"Assignment ID {assignment_id} does not exist.")

    cursor.execute("""
        UPDATE delivery_assignments
        SET driver_id = ?,
            vehicle_id = ?,
            route_details = ?,
            delivery_date = ?,
            dispatch_time = ?,
            arrival_time = ?,
            assignment_status = ?
        WHERE assignment_id = ?
    """, (
        driver_id,
        vehicle_id,
        route_details,
        delivery_date,
        dispatch_time,
        arrival_time,
        assignment_status,
        assignment_id
    ))

    conn.commit()
    conn.close()

    log_audit(
        user_id,
        "UPDATE",
        "delivery_assignments",
        assignment_id,
        f"Updated delivery assignment {assignment_id}"
    )

def assign_delivery(shipment_id, driver_id, vehicle_id, route_details,
                    delivery_date, dispatch_time, arrival_time,
                    assignment_status, user_id=1):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO delivery_assignments (
            shipment_id, driver_id, vehicle_id, route_details,
            delivery_date, dispatch_time, arrival_time, assignment_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        shipment_id, driver_id, vehicle_id, route_details,
        delivery_date, dispatch_time, arrival_time, assignment_status
    ))

    assignment_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(
        user_id,
        "INSERT",
        "delivery_assignments",
        assignment_id,
        f"Assigned shipment {shipment_id} to driver {driver_id} and vehicle {vehicle_id}"
    )

def get_all_delivery_assignments():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT assignment_id, shipment_id, driver_id, vehicle_id,
               route_details, delivery_date, dispatch_time,
               arrival_time, assignment_status
        FROM delivery_assignments
        ORDER BY assignment_id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows