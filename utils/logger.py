from datetime import datetime
from database.db import get_connection

def log_audit(user_id, action_type, table_name, record_id, details=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit_logs (user_id, action_type, table_name, record_id, action_time, details)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, action_type, table_name, record_id, datetime.now().isoformat(), details))

    conn.commit()
    conn.close()