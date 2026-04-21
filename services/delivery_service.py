from database.db import get_connection
from utils.logger import log_audit
from utils.validation import (
    validate_required,
    validate_choice,
    validate_date,
    validate_record_exists,
    validate_time,
    ALLOWED_ASSIGNMENT_STATUSES
)


def assign_delivery(shipment_id, driver_id, vehicle_id, route_details,
                    delivery_date, dispatch_time, arrival_time,
                    assignment_status, user_id=1):

    validate_record_exists("shipments", "shipment_id", shipment_id, "Shipment ID")
    validate_record_exists("drivers", "driver_id", driver_id, "Driver ID")
    validate_record_exists("vehicles", "vehicle_id", vehicle_id, "Vehicle ID")
    validate_required(route_details, "Route details")
    validate_date(delivery_date, "Delivery date")
    validate_choice(assignment_status, "Assignment status", ALLOWED_ASSIGNMENT_STATUSES)
    validate_time(dispatch_time, "Dispatch time", allow_blank=True)
    validate_time(arrival_time, "Arrival time", allow_blank=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO delivery_assignments (
            shipment_id, driver_id, vehicle_id, route_details,
            delivery_date, dispatch_time, arrival_time, assignment_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        shipment_id,
        driver_id,
        vehicle_id,
        route_details.strip(),
        delivery_date,
        (dispatch_time or "").strip(),
        (arrival_time or "").strip(),
        assignment_status
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


def update_delivery_assignment(assignment_id, driver_id, vehicle_id, route_details,
                               delivery_date, dispatch_time, arrival_time,
                               assignment_status, user_id=1):

    validate_record_exists("delivery_assignments", "assignment_id", assignment_id, "Assignment ID")
    validate_record_exists("drivers", "driver_id", driver_id, "Driver ID")
    validate_record_exists("vehicles", "vehicle_id", vehicle_id, "Vehicle ID")
    validate_required(route_details, "Route details")
    validate_date(delivery_date, "Delivery date")
    validate_choice(assignment_status, "Assignment status", ALLOWED_ASSIGNMENT_STATUSES)
    validate_time(dispatch_time, "Dispatch time", allow_blank=True)
    validate_time(arrival_time, "Arrival time", allow_blank=True)

    conn = get_connection()
    cursor = conn.cursor()

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
        route_details.strip(),
        delivery_date,
        (dispatch_time or "").strip(),
        (arrival_time or "").strip(),
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