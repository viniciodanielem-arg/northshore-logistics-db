from database.db import get_connection
from utils.logger import log_audit
from utils.security import simple_encrypt
from utils.validation import (
    validate_positive_number,
    validate_date,
    validate_record_exists
)

def add_payment(shipment_id, amount_due, amount_paid, payment_method,
                payment_date, user_id=1):
    validate_record_exists("shipments", "shipment_id", shipment_id, "Shipment ID")
    validate_positive_number(amount_due, "Amount due", allow_zero=True)
    validate_positive_number(amount_paid, "Amount paid")
    validate_date(payment_date, "Payment date")

    amount_due = float(amount_due)
    amount_paid = float(amount_paid)

    if amount_paid > amount_due:
        raise ValueError("Amount paid cannot be greater than amount due.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount_paid), 0), MIN(amount_due), MAX(amount_due)
        FROM payments
        WHERE shipment_id = ?
    """, (shipment_id,))
    total_paid_so_far, min_due, max_due = cursor.fetchone()

    total_paid_so_far = float(total_paid_so_far or 0)

    if min_due is not None and max_due is not None:
        if float(min_due) != float(max_due):
            conn.close()
            raise ValueError(
                "Existing payment records for this shipment have inconsistent amount due values."
            )

        if amount_due != float(min_due):
            conn.close()
            raise ValueError(
                f"Amount due must match the existing value for this shipment ({float(min_due):.2f})."
            )

    if total_paid_so_far >= amount_due:
        conn.close()
        raise ValueError("This shipment has already been fully paid.")

    new_total_paid = total_paid_so_far + amount_paid

    if new_total_paid > amount_due:
        conn.close()
        raise ValueError(
            f"Cannot add payment. Total paid would become {new_total_paid:.2f}, "
            f"which exceeds the amount due of {amount_due:.2f}."
        )

    if new_total_paid < amount_due:
        calculated_status = "Partially Paid"
    else:
        calculated_status = "Paid"

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
        calculated_status
    ))

    payment_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(
        user_id,
        "INSERT",
        "payments",
        payment_id,
        f"Added payment for shipment {shipment_id} with status {calculated_status}"
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


def update_payment_status(payment_id, user_id=1):
    conn = get_connection()
    cursor = conn.cursor()

    # Find the shipment and this payment's amount_due
    cursor.execute("""
        SELECT shipment_id, amount_due
        FROM payments
        WHERE payment_id = ?
    """, (payment_id,))
    payment = cursor.fetchone()

    if not payment:
        conn.close()
        raise ValueError(f"Payment ID {payment_id} does not exist.")

    shipment_id, amount_due = payment
    amount_due = float(amount_due)

    # Calculate total paid for the whole shipment
    cursor.execute("""
        SELECT COALESCE(SUM(amount_paid), 0)
        FROM payments
        WHERE shipment_id = ?
    """, (shipment_id,))
    total_paid = float(cursor.fetchone()[0] or 0)

    # Work out the correct status automatically
    if total_paid <= 0:
        calculated_status = "Pending"
    elif total_paid < amount_due:
        calculated_status = "Partially Paid"
    elif total_paid == amount_due:
        calculated_status = "Paid"
    else:
        conn.close()
        raise ValueError(
            f"Total paid for shipment {shipment_id} exceeds the amount due."
        )

    # Update all payment rows for this shipment so they stay consistent
    cursor.execute("""
        UPDATE payments
        SET payment_status = ?
        WHERE shipment_id = ?
    """, (calculated_status, shipment_id))

    conn.commit()
    conn.close()

    log_audit(
        user_id,
        "UPDATE",
        "payments",
        payment_id,
        f"Recalculated payment status for shipment {shipment_id} as {calculated_status}"
    )