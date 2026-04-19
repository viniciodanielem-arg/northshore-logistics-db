from database.db import get_connection
from utils.logger import log_audit


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

    log_audit(user_id, "INSERT", "delivery_assignments", assignment_id,
              f"Assigned shipment {shipment_id} to driver {driver_id} and vehicle {vehicle_id}")