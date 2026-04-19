from database.db import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        role_id INTEGER NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT,
        is_active INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (role_id) REFERENCES roles(role_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        address_encrypted TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warehouses (
        warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
        warehouse_name TEXT NOT NULL,
        city TEXT,
        address TEXT,
        manager_name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        description TEXT,
        category TEXT,
        unit_price REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warehouse_inventory (
        warehouse_inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
        warehouse_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        reorder_level INTEGER NOT NULL,
        item_location TEXT,
        FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
        FOREIGN KEY (item_id) REFERENCES inventory_items(item_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
        registration_number TEXT NOT NULL UNIQUE,
        vehicle_type TEXT,
        capacity REAL,
        maintenance_due_date TEXT,
        availability_status TEXT,
        assigned_warehouse_id INTEGER,
        FOREIGN KEY (assigned_warehouse_id) REFERENCES warehouses(warehouse_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
        driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone TEXT,
        license_number TEXT NOT NULL UNIQUE,
        license_expiry TEXT,
        route_history_notes TEXT,
        shift_assignment TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipments (
        shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT NOT NULL UNIQUE,
        sender_customer_id INTEGER NOT NULL,
        receiver_customer_id INTEGER NOT NULL,
        item_description TEXT NOT NULL,
        origin_warehouse_id INTEGER NOT NULL,
        destination_address_encrypted TEXT NOT NULL,
        created_date TEXT NOT NULL,
        current_status TEXT NOT NULL,
        transport_cost REAL,
        surcharge REAL,
        payment_status TEXT,
        FOREIGN KEY (sender_customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (receiver_customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (origin_warehouse_id) REFERENCES warehouses(warehouse_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS delivery_assignments (
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        shipment_id INTEGER NOT NULL,
        driver_id INTEGER NOT NULL,
        vehicle_id INTEGER NOT NULL,
        route_details TEXT,
        delivery_date TEXT,
        dispatch_time TEXT,
        arrival_time TEXT,
        assignment_status TEXT,
        FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id),
        FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incident_reports (
        incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
        shipment_id INTEGER NOT NULL,
        incident_type TEXT NOT NULL,
        description TEXT,
        reported_by_user_id INTEGER NOT NULL,
        incident_date TEXT NOT NULL,
        resolution_status TEXT NOT NULL,
        FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id),
        FOREIGN KEY (reported_by_user_id) REFERENCES users(user_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        shipment_id INTEGER NOT NULL,
        amount_due REAL NOT NULL,
        amount_paid REAL,
        payment_method TEXT,
        payment_date TEXT,
        payment_status TEXT NOT NULL,
        FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warehouse_activity_logs (
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        warehouse_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        activity_type TEXT NOT NULL,
        quantity_changed INTEGER NOT NULL,
        activity_date TEXT NOT NULL,
        notes TEXT,
        recorded_by_user_id INTEGER NOT NULL,
        FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
        FOREIGN KEY (item_id) REFERENCES inventory_items(item_id),
        FOREIGN KEY (recorded_by_user_id) REFERENCES users(user_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        action_type TEXT NOT NULL,
        table_name TEXT NOT NULL,
        record_id INTEGER NOT NULL,
        action_time TEXT NOT NULL,
        details TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    conn.commit()
    conn.close()