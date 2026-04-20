from datetime import datetime
from database.db import get_connection
from utils.security import simple_encrypt
from utils.logger import log_audit


def record_exists(cursor, table_name, id_field, record_id):
    query = f"SELECT 1 FROM {table_name} WHERE {id_field} = ?"
    cursor.execute(query, (record_id,))
    return cursor.fetchone() is not None


def validate_shipment_data(order_number, item_description, transport_cost, surcharge,
                           sender_customer_id, receiver_customer_id, origin_warehouse_id):
    if not order_number.strip():
        return False, "Order number is required."

    if not item_description.strip():
        return False, "Item description is required."

    if transport_cost < 0:
        return False, "Transport cost cannot be negative."

    if surcharge < 0:
        return False, "Surcharge cannot be negative."

    conn = get_connection()
    cursor = conn.cursor()

    sender_exists = record_exists(cursor, "customers", "customer_id", sender_customer_id)
    receiver_exists = record_exists(cursor, "customers", "customer_id", receiver_customer_id)
    warehouse_exists = record_exists(cursor, "warehouses", "warehouse_id", origin_warehouse_id)

    conn.close()

    if not sender_exists:
        return False, f"Sender customer ID {sender_customer_id} does not exist."

    if not receiver_exists:
        return False, f"Receiver customer ID {receiver_customer_id} does not exist."

    if not warehouse_exists:
        return False, f"Warehouse ID {origin_warehouse_id} does not exist."

    return True, "Valid"


def add_shipment(order_number, sender_customer_id, receiver_customer_id,
                 item_description, origin_warehouse_id, destination_address,
                 transport_cost, surcharge, payment_status, user_id=None):
    valid, message = validate_shipment_data(
        order_number,
        item_description,
        transport_cost,
        surcharge,
        sender_customer_id,
        receiver_customer_id,
        origin_warehouse_id
    )

    if not valid:
        raise ValueError(message)

    conn = get_connection()
    cursor = conn.cursor()

    encrypted_address = simple_encrypt(destination_address)

    cursor.execute("""
        INSERT INTO shipments (
            order_number, sender_customer_id, receiver_customer_id,
            item_description, origin_warehouse_id,
            destination_address_encrypted, created_date,
            current_status, transport_cost, surcharge, payment_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        order_number,
        sender_customer_id,
        receiver_customer_id,
        item_description,
        origin_warehouse_id,
        encrypted_address,
        datetime.now().date().isoformat(),
        "In Transit",
        transport_cost,
        surcharge,
        payment_status
    ))

    shipment_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(user_id, "INSERT", "shipments", shipment_id, f"Added shipment {order_number}")


def get_all_shipments():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT shipment_id, order_number, sender_customer_id, receiver_customer_id,
               item_description, origin_warehouse_id, created_date,
               current_status, transport_cost, surcharge, payment_status
        FROM shipments
        ORDER BY shipment_id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def update_shipment_status(shipment_id, new_status, user_id=None):
    if not new_status.strip():
        raise ValueError("New status is required.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT shipment_id FROM shipments WHERE shipment_id = ?", (shipment_id,))
    shipment = cursor.fetchone()

    if not shipment:
        conn.close()
        raise ValueError(f"Shipment ID {shipment_id} does not exist.")

    cursor.execute("""
        UPDATE shipments
        SET current_status = ?
        WHERE shipment_id = ?
    """, (new_status, shipment_id))

    conn.commit()
    conn.close()

    log_audit(user_id, "UPDATE", "shipments", shipment_id, f"Changed status to {new_status}")