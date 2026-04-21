from datetime import datetime
from database.db import get_connection
from utils.security import simple_encrypt
from utils.logger import log_audit
from utils.validation import (
    validate_required,
    validate_positive_number,
    validate_choice,
    validate_record_exists,
    validate_text_length,
    ALLOWED_SHIPMENT_STATUSES,
    ALLOWED_PAYMENT_STATUSES
)


def validate_shipment_data(order_number, item_description, transport_cost, surcharge,
                           sender_customer_id, receiver_customer_id,
                           origin_warehouse_id, destination_address, payment_status):
    validate_required(order_number, "Order number")
    validate_required(item_description, "Item description")
    validate_required(destination_address, "Destination address")

    validate_text_length(order_number, "Order number", 50)
    validate_text_length(item_description, "Item description", 255)
    validate_text_length(destination_address, "Destination address", 255)

    validate_positive_number(transport_cost, "Transport cost", allow_zero=True)
    validate_positive_number(surcharge, "Surcharge", allow_zero=True)

    validate_record_exists("customers", "customer_id", sender_customer_id, "Sender customer ID")
    validate_record_exists("customers", "customer_id", receiver_customer_id, "Receiver customer ID")
    validate_record_exists("warehouses", "warehouse_id", origin_warehouse_id, "Warehouse ID")

    validate_choice(payment_status, "Payment status", ALLOWED_PAYMENT_STATUSES)


def add_shipment(order_number, sender_customer_id, receiver_customer_id,
                 item_description, origin_warehouse_id, destination_address,
                 transport_cost, surcharge, payment_status, user_id=None):

    validate_shipment_data(
        order_number,
        item_description,
        transport_cost,
        surcharge,
        sender_customer_id,
        receiver_customer_id,
        origin_warehouse_id,
        destination_address,
        payment_status
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT shipment_id FROM shipments WHERE order_number = ?", (order_number,))
    if cursor.fetchone():
        conn.close()
        raise ValueError("Order number already exists.")

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
        order_number.strip(),
        sender_customer_id,
        receiver_customer_id,
        (item_description or "").strip(),
        origin_warehouse_id,
        encrypted_address,
        datetime.now().date().isoformat(),
        "In Transit",
        float(transport_cost),
        float(surcharge),
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
    validate_choice(new_status, "Shipment status", ALLOWED_SHIPMENT_STATUSES)

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

def search_shipments_by_order(order_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT shipment_id, order_number, sender_customer_id,
               receiver_customer_id, item_description,
               origin_warehouse_id, created_date,
               current_status, transport_cost, surcharge, payment_status
        FROM shipments
        WHERE order_number LIKE ?
        ORDER BY shipment_id DESC
    """, (f"%{order_number}%",))

    rows = cursor.fetchall()
    conn.close()
    return rows


def filter_shipments_by_status(status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT shipment_id, order_number, sender_customer_id,
               receiver_customer_id, item_description,
               origin_warehouse_id, created_date,
               current_status, transport_cost, surcharge, payment_status
        FROM shipments
        WHERE current_status = ?
        ORDER BY shipment_id DESC
    """, (status,))

    rows = cursor.fetchall()
    conn.close()
    return rows