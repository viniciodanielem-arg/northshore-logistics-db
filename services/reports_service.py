from database.db import get_connection


def get_shipment_status_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT current_status, COUNT(*)
        FROM shipments
        GROUP BY current_status
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_vehicle_utilisation_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.registration_number, COUNT(d.assignment_id) AS total_assignments
        FROM vehicles v
        LEFT JOIN delivery_assignments d ON v.vehicle_id = d.vehicle_id
        GROUP BY v.vehicle_id, v.registration_number
        ORDER BY total_assignments DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_warehouse_activity_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT w.warehouse_name, wal.activity_type, wal.quantity_changed, wal.activity_date
        FROM warehouse_activity_logs wal
        JOIN warehouses w ON wal.warehouse_id = w.warehouse_id
        ORDER BY wal.activity_date DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows