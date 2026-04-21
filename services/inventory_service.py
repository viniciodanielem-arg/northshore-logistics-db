from datetime import datetime
from database.db import get_connection
from utils.logger import log_audit
from utils.validation import (
    validate_required,
    validate_integer,
    validate_positive_number,
    validate_record_exists,
    validate_text_length
)


def add_inventory_item(item_name, description, category, unit_price, user_id=1):
    validate_required(item_name, "Item name")
    validate_required(category, "Category")
    validate_positive_number(unit_price, "Unit price", allow_zero=True)

    validate_text_length(item_name, "Item name", 100)
    validate_text_length(description, "Description", 255)
    validate_text_length(category, "Category", 100)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO inventory_items (item_name, description, category, unit_price)
        VALUES (?, ?, ?, ?)
    """, (
        item_name.strip(),
        (description or "").strip(),
        category.strip(),
        float(unit_price)
    ))

    item_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(user_id, "INSERT", "inventory_items", item_id, f"Added item {item_name}")


def add_warehouse_inventory(warehouse_id, item_id, quantity, reorder_level,
                            item_location, recorded_by_user_id=1):

    validate_record_exists("warehouses", "warehouse_id", warehouse_id, "Warehouse ID")
    validate_record_exists("inventory_items", "item_id", item_id, "Item ID")
    validate_integer(quantity, "Quantity", allow_zero=True)
    validate_integer(reorder_level, "Reorder level", allow_zero=True)
    validate_required(item_location, "Item location")
    validate_text_length(item_location, "Item location", 100)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT warehouse_inventory_id
        FROM warehouse_inventory
        WHERE warehouse_id = ? AND item_id = ?
    """, (warehouse_id, item_id))

    existing = cursor.fetchone()
    if existing:
        conn.close()
        raise ValueError("This item already exists in this warehouse inventory record.")

    cursor.execute("""
        INSERT INTO warehouse_inventory (
            warehouse_id, item_id, quantity, reorder_level, item_location
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        warehouse_id,
        item_id,
        int(quantity),
        int(reorder_level),
        item_location.strip()
    ))

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
        int(quantity),
        datetime.now().isoformat(),
        f"Initial stock added at {item_location.strip()}",
        recorded_by_user_id
    ))

    conn.commit()
    conn.close()

    log_audit(
        recorded_by_user_id,
        "INSERT",
        "warehouse_inventory",
        warehouse_inventory_id,
        f"Added inventory item {item_id} to warehouse {warehouse_id}"
    )


def update_inventory_quantity(warehouse_id, item_id, quantity_change, user_id=1):
    validate_record_exists("warehouses", "warehouse_id", warehouse_id, "Warehouse ID")
    validate_record_exists("inventory_items", "item_id", item_id, "Item ID")

    try:
        quantity_change = int(quantity_change)
    except (TypeError, ValueError):
        raise ValueError("Quantity change must be a valid whole number.")

    if quantity_change == 0:
        raise ValueError("Quantity change cannot be 0.")

    conn = get_connection()
    cursor = conn.cursor()

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

    cursor.execute("""
        UPDATE warehouse_inventory
        SET quantity = ?
        WHERE warehouse_id = ? AND item_id = ?
    """, (new_quantity, warehouse_id, item_id))

    activity_type = "RESTOCK" if quantity_change > 0 else "STOCK_OUT"

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


def transfer_inventory(item_id, from_warehouse, to_warehouse, quantity, user_id=1):
    validate_record_exists("inventory_items", "item_id", item_id, "Item ID")
    validate_record_exists("warehouses", "warehouse_id", from_warehouse, "Source warehouse ID")
    validate_record_exists("warehouses", "warehouse_id", to_warehouse, "Destination warehouse ID")

    quantity = validate_integer(quantity, "Transfer quantity")

    if from_warehouse == to_warehouse:
        raise ValueError("Source and destination warehouses must be different.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT quantity, reorder_level, item_location
        FROM warehouse_inventory
        WHERE warehouse_id = ? AND item_id = ?
    """, (from_warehouse, item_id))

    source = cursor.fetchone()
    if not source:
        conn.close()
        raise ValueError("Item does not exist in source warehouse.")

    source_quantity = source[0]
    if source_quantity < quantity:
        conn.close()
        raise ValueError("Not enough stock in source warehouse.")

    cursor.execute("""
        UPDATE warehouse_inventory
        SET quantity = quantity - ?
        WHERE warehouse_id = ? AND item_id = ?
    """, (quantity, from_warehouse, item_id))

    cursor.execute("""
        SELECT warehouse_inventory_id
        FROM warehouse_inventory
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

    now = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO warehouse_activity_logs (
            warehouse_id, item_id, activity_type,
            quantity_changed, activity_date, notes, recorded_by_user_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        from_warehouse,
        item_id,
        "TRANSFER_OUT",
        quantity,
        now,
        f"Transferred to warehouse {to_warehouse}",
        user_id
    ))

    cursor.execute("""
        INSERT INTO warehouse_activity_logs (
            warehouse_id, item_id, activity_type,
            quantity_changed, activity_date, notes, recorded_by_user_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        to_warehouse,
        item_id,
        "TRANSFER_IN",
        quantity,
        now,
        f"Received from warehouse {from_warehouse}",
        user_id
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