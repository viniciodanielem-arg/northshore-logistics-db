from datetime import datetime
from database.db import get_connection
from utils.logger import log_audit


def add_inventory_item(item_name, description, category, unit_price, user_id=1):
    if not item_name.strip():
        raise ValueError("Item name is required.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO inventory_items (item_name, description, category, unit_price)
        VALUES (?, ?, ?, ?)
    """, (item_name, description, category, unit_price))

    item_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(user_id, "INSERT", "inventory_items", item_id, f"Added item {item_name}")


def add_warehouse_inventory(warehouse_id, item_id, quantity, reorder_level,
                            item_location, recorded_by_user_id=1):
    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")
    if reorder_level < 0:
        raise ValueError("Reorder level cannot be negative.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO warehouse_inventory (
            warehouse_id, item_id, quantity, reorder_level, item_location
        )
        VALUES (?, ?, ?, ?, ?)
    """, (warehouse_id, item_id, quantity, reorder_level, item_location))

    warehouse_inventory_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO warehouse_activity_logs (
            warehouse_id, item_id, activity_type, quantity_changed,
            activity_date, notes, recorded_by_user_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        warehouse_id,
        item_id,
        "STOCK_ADDED",
        quantity,
        datetime.now().isoformat(),
        f"Initial stock added at {item_location}",
        recorded_by_user_id
    ))

    conn.commit()
    conn.close()

    log_audit(recorded_by_user_id, "INSERT", "warehouse_inventory",
              warehouse_inventory_id, f"Added inventory item {item_id} to warehouse {warehouse_id}")


def get_inventory_by_warehouse():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT wi.warehouse_inventory_id,
               w.warehouse_name,
               i.item_name,
               wi.quantity,
               wi.reorder_level,
               wi.item_location
        FROM warehouse_inventory wi
        JOIN warehouses w ON wi.warehouse_id = w.warehouse_id
        JOIN inventory_items i ON wi.item_id = i.item_id
        ORDER BY wi.warehouse_inventory_id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows