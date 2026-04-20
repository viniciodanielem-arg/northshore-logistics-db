from datetime import datetime
from database.db import get_connection
from utils.logger import log_audit


def add_incident(shipment_id, incident_type, description,
                 reported_by_user_id, resolution_status):
    if not incident_type.strip():
        raise ValueError("Incident type is required.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO incident_reports (
            shipment_id, incident_type, description,
            reported_by_user_id, incident_date, resolution_status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        shipment_id,
        incident_type,
        description,
        reported_by_user_id,
        datetime.now().isoformat(),
        resolution_status
    ))

    incident_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(reported_by_user_id, "INSERT", "incident_reports",
              incident_id, f"Incident added for shipment {shipment_id}")