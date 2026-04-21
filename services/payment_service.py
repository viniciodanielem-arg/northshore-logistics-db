from database.db import get_connection
from utils.logger import log_audit
from utils.security import simple_encrypt


def add_payment(shipment_id, amount_due, amount_paid, payment_method,
                payment_date, payment_status, user_id=1):
    if amount_due < 0:
        raise ValueError("Amount due cannot be negative.")
    if amount_paid < 0:
        raise ValueError("Amount paid cannot be negative.")
    if not payment_status.strip():
        raise ValueError("Payment status is required.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT shipment_id FROM shipments WHERE shipment_id = ?", (shipment_id,))
    shipment = cursor.fetchone()
    if not shipment:
        conn.close()
        raise ValueError(f"Shipment ID {shipment_id} does not exist.")

    encrypted_method = simple_encrypt(payment_method)

    cursor.execute("""
    INSERT INTO payments (
        shipment_id, amount_due, amount_paid,
        payment_method, payment_date, payment_status
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        shipment_id,
        amount_due,
        amount_paid,
        encrypted_method,
        payment_date,
        payment_status
    ))

    payment_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(
        user_id,
        "INSERT",
        "payments",
        payment_id,
        f"Added payment for shipment {shipment_id}"
    )


def get_all_payments():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT payment_id, shipment_id, amount_due, amount_paid,
               payment_method, payment_date, payment_status
        FROM payments
        ORDER BY payment_id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def update_payment_status(payment_id, new_status, user_id=1):
    if not new_status.strip():
        raise ValueError("New payment status is required.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT payment_id FROM payments WHERE payment_id = ?", (payment_id,))
    payment = cursor.fetchone()
    if not payment:
        conn.close()
        raise ValueError(f"Payment ID {payment_id} does not exist.")

    cursor.execute("""
        UPDATE payments
        SET payment_status = ?
        WHERE payment_id = ?
    """, (new_status, payment_id))

    conn.commit()
    conn.close()

    log_audit(
        user_id,
        "UPDATE",
        "payments",
        payment_id,
        f"Changed payment status to {new_status}"
    )