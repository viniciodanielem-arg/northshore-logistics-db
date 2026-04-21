from datetime import datetime
from database.db import get_connection
from utils.logger import log_audit
from utils.validation import (
    validate_required,
    validate_choice,
    validate_record_exists,
    validate_text_length,
    ALLOWED_INCIDENT_STATUSES
)


def add_incident(shipment_id, incident_type, description,
                 reported_by_user_id, resolution_status):

    validate_record_exists("shipments", "shipment_id", shipment_id, "Shipment ID")
    validate_record_exists("users", "user_id", reported_by_user_id, "Reported by user ID")
    validate_required(incident_type, "Incident type")
    validate_required(description, "Description")
    validate_choice(resolution_status, "Resolution status", ALLOWED_INCIDENT_STATUSES)

    validate_text_length(incident_type, "Incident type", 100)
    validate_text_length(description, "Description", 500)

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
        incident_type.strip(),
        (description or "").strip(),
        reported_by_user_id,
        datetime.now().isoformat(),
        resolution_status
    ))

    incident_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(
        reported_by_user_id,
        "INSERT",
        "incident_reports",
        incident_id,
        f"Incident added for shipment {shipment_id}"
    )


def get_all_incidents():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT incident_id, shipment_id, incident_type, description,
               reported_by_user_id, incident_date, resolution_status
        FROM incident_reports
        ORDER BY incident_id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows