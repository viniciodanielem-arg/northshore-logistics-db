from datetime import datetime
from database.db import get_connection
from utils.security import simple_encrypt

def add_shipment(order_number, sender_customer_id, reciever_customer_id,
                 item_description, origin_warehouse_id, destination_address,
                 transport_cost, surcharge, payment_status):
    conn = get_connection()
    cursor = conn.cursor()

    encrypted_address = simple_encrypt(destination_address)

    cursor.execute("""
        INSERT INTO shipments (
            order_number, sender_customer_id, recieve_customer_id,
            item_description, origin_warehouse_id,
            destination_address_encrypted, created_date,
            current_status, transport_cost, surcharge, payment_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        order_number,
        sender_customer_id,
        reciever_customer_id,
        item_description,
        origin_warehouse_id,
        encrypted_address,
        datetime.now().date().isoformat(),
        "In Transit",
        transport_cost,
        surcharge,
        payment_status
    ))

    conn.commit()
    conn.close()