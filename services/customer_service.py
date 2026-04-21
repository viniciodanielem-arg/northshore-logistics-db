from database.db import get_connection
from utils.security import simple_encrypt
from utils.logger import log_audit
from utils.validation import (
    validate_required,
    validate_email,
    validate_phone,
    validate_text_length
)


def add_customer(customer_name, phone, email, address, user_id=1):
    validate_required(customer_name, "Customer name")
    validate_required(address, "Address")
    validate_phone(phone, allow_blank=True)
    validate_email(email, allow_blank=True)
    validate_text_length(customer_name, "Customer name", 100)
    validate_text_length(address, "Address", 255)

    conn = get_connection()
    cursor = conn.cursor()
    encrypted_address = simple_encrypt(address)

    cursor.execute("""
        INSERT INTO customers (customer_name, phone, email, address_encrypted)
        VALUES (?, ?, ?, ?)
    """, (customer_name.strip(), phone.strip(), email.strip(), encrypted_address))

    customer_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(user_id, "INSERT", "customers", customer_id, f"Added customer {customer_name}")

def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id, customer_name, phone, email
        FROM customers
        ORDER BY customer_id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows