from database.db import get_connection
from utils.logger import log_audit

def add_warehouse(warehouse_name, city, address, manager_name, user_id=1):
    if not warehouse_name.strip():
        raise ValueError("Warehouse name is required.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO warehouses (warehouse_name, city, address, manager_name)
        VALUES (?, ?, ?, ?)
    """, (warehouse_name, city, address, manager_name))

    warehouse_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(user_id, "INSERT", "warehouses", warehouse_id, f"Added warehouse {warehouse_name}")

def get_all_warehouses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT warehouse_id, warehouse_name, city, address, manager_name
        FROM warehouses
        ORDER BY warehpuse_id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows