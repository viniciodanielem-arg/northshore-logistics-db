from datetime import datetime
from database.db import get_connection
from utils.logger import log_audit

def update_inventory_quantity(warehouse_id, item_id, quantity_change, user_id=1):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if record exists
    cursor.execute("""
        SELECT quantity FROM warehouse_inventory
        WHERE warehouse_id = ? AND item_id = ?
    """, (warehouse_id, item_id))

    record = cursor.fetchone()

    if not record:
        conn.close()
        raise ValueError("Inventory record does not exist.")

    current_quantity = record[0]
    new_quantity = current_quantity + quantity_change

    if new_quantity < 0:
        conn.close()
        raise ValueError("Not enough stock available.")

    # Update inventory
    cursor.execute("""
        UPDATE warehouse_inventory
        SET quantity = ?
        WHERE warehouse_id = ? AND item_id = ?
    """, (new_quantity, warehouse_id, item_id))

    # Determine activity type
    if quantity_change > 0:
        activity_type = "RESTOCK"
    else:
        activity_type = "STOCK_OUT"

    # Log activity
    cursor.execute("""
        INSERT INTO warehouse_activity_logs (
            warehouse_id, item_id, activity_type,
            quantity_changed, activity_date, notes, recorded_by_user_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        warehouse_id,
        item_id,
        activity_type,
        abs(quantity_change),
        datetime.now().isoformat(),
        f"Stock updated (change: {quantity_change})",
        user_id
    ))

    conn.commit()
    conn.close()

    log_audit(
        user_id,
        "UPDATE",
        "warehouse_inventory",
        item_id,
        f"Quantity changed by {quantity_change} in warehouse {warehouse_id}"
    )

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

def transfer_inventory(item_id, from_warehouse, to_warehouse, quantity, user_id=1):
    if quantity <= 0:
        raise ValueError("Transfer quantity must be positive.")

    conn = get_connection()
    cursor = conn.cursor()

    # Remove from source
    cursor.execute("""
        SELECT quantity FROM warehouse_inventory
        WHERE warehouse_id = ? AND item_id = ?
    """, (from_warehouse, item_id))

    source = cursor.fetchone()

    if not source or source[0] < quantity:
        conn.close()
        raise ValueError("Not enough stock in source warehouse.")

    cursor.execute("""
        UPDATE warehouse_inventory
        SET quantity = quantity - ?
        WHERE warehouse_id = ? AND item_id = ?
    """, (quantity, from_warehouse, item_id))

    # Add to destination (create if not exists)
    cursor.execute("""
        SELECT quantity FROM warehouse_inventory
        WHERE warehouse_id = ? AND item_id = ?
    """, (to_warehouse, item_id))

    dest = cursor.fetchone()

    if dest:
        cursor.execute("""
            UPDATE warehouse_inventory
            SET quantity = quantity + ?
            WHERE warehouse_id = ? AND item_id = ?
        """, (quantity, to_warehouse, item_id))
    else:
        cursor.execute("""
            INSERT INTO warehouse_inventory (
                warehouse_id, item_id, quantity, reorder_level, item_location
            )
            VALUES (?, ?, ?, ?, ?)
        """, (to_warehouse, item_id, quantity, 10, "Transferred"))

    # Log BOTH actions
    now = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO warehouse_activity_logs (
            warehouse_id, item_id, activity_type,
            quantity_changed, activity_date, notes, recorded_by_user_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        from_warehouse, item_id, "TRANSFER_OUT",
        quantity, now, f"Transferred to warehouse {to_warehouse}", user_id
    ))

    cursor.execute("""
        INSERT INTO warehouse_activity_logs (
            warehouse_id, item_id, activity_type,
            quantity_changed, activity_date, notes, recorded_by_user_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        to_warehouse, item_id, "TRANSFER_IN",
        quantity, now, f"Received from warehouse {from_warehouse}", user_id
    ))

    conn.commit()
    conn.close()

    log_audit(
        user_id,
        "TRANSFER",
        "warehouse_inventory",
        item_id,
        f"Transferred {quantity} from {from_warehouse} to {to_warehouse}"
    )