from database.db import get_connection
from utils.security import simple_encrypt
from utils.logger import log_audit

def add_customer(customer_name, phone, email, address, user_id=1):
    if not customer_name.strip():
        raise ValueError("Customer name is required.")
    if not address.strip():
        raise ValueError("Address is required.")

    conn = get_connection()
    cursor = conn.cursor()

    encrypted_address = simple_encrypt(address)

    cursor.execute("""
        INSERT INTO customers (customer_name, phone, email, address_encrypted)
        VALUES (?, ?, ?, ?)
        """, (customer_name, phone, email, encrypted_address))

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