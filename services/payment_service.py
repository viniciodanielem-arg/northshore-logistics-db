from database.db import get_connection
from utils.logger import log_audit
from utils.security import simple_encrypt
from utils.validation import (
    validate_positive_number,
    validate_choice,
    validate_date,
    validate_record_exists,
    ALLOWED_PAYMENT_STATUSES
)


def add_payment(shipment_id, amount_due, amount_paid, payment_method,
                payment_date, payment_status, user_id=1):

    validate_record_exists("shipments", "shipment_id", shipment_id, "Shipment ID")
    validate_positive_number(amount_due, "Amount due", allow_zero=True)
    validate_positive_number(amount_paid, "Amount paid", allow_zero=True)
    validate_choice(payment_status, "Payment status", ALLOWED_PAYMENT_STATUSES)
    validate_date(payment_date, "Payment date")

    if float(amount_paid) > float(amount_due):
        raise ValueError("Amount paid cannot be greater than amount due.")

    conn = get_connection()
    cursor = conn.cursor()

    encrypted_method = simple_encrypt(payment_method)

    cursor.execute("""
        INSERT INTO payments (
            shipment_id, amount_due, amount_paid,
            payment_method, payment_date, payment_status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        shipment_id,
        float(amount_due),
        float(amount_paid),
        encrypted_method,
        payment_date,
        payment_status
    ))

    payment_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(user_id, "INSERT", "payments", payment_id, f"Added payment for shipment {shipment_id}")


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
    validate_choice(new_status, "Payment status", ALLOWED_PAYMENT_STATUSES)

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

    log_audit(user_id, "UPDATE", "payments", payment_id, f"Changed payment status to {new_status}")