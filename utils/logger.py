from datetime import datetime
from database.db import get_connection


def log_audit(user_id, action_type, table_name, record_id, details=""):
    if user_id is None:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    user_exists = cursor.fetchone()

    if not user_exists:
        conn.close()
        return

    cursor.execute("""
        INSERT INTO audit_logs (user_id, action_type, table_name, record_id, action_time, details)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, action_type, table_name, record_id, datetime.now().isoformat(), details))

    conn.commit()
    conn.close()