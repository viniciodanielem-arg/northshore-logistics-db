import tkinter as tk
from tkinter import messagebox
from typing import Optional
from tkinter import Entry, Text, Tk

from services.auth_service import login_user, register_user, get_all_users
from services.shipment_service import add_shipment, get_all_shipments, update_shipment_status
from services.customer_service import add_customer, get_all_customers
from services.warehouse_service import add_warehouse, get_all_warehouses
from services.vehicle_service import add_vehicle, get_all_vehicles
from services.driver_service import add_driver, get_all_drivers
from services.inventory_service import add_inventory_item, add_warehouse_inventory, get_inventory_by_warehouse
from services.delivery_service import assign_delivery, get_all_delivery_assignments
from services.incident_service import add_incident, get_all_incidents
from services.reports_service import (
    get_shipment_status_report,
    get_vehicle_utilisation_report,
    get_warehouse_activity_report
)

from utils.access_control import has_role, require_role

current_user: Optional[dict] = None
output_box: Optional[Text] = None

customer_name_entry: Optional[Entry] = None
customer_phone_entry: Optional[Entry] = None
customer_email_entry: Optional[Entry] = None
customer_address_entry: Optional[Entry] = None

warehouse_name_entry: Optional[Entry] = None
warehouse_city_entry: Optional[Entry] = None
warehouse_address_entry: Optional[Entry] = None
warehouse_manager_entry: Optional[Entry] = None

order_entry: Optional[Entry] = None
sender_entry: Optional[Entry] = None
receiver_entry: Optional[Entry] = None
item_entry: Optional[Entry] = None
warehouse_entry: Optional[Entry] = None
address_entry: Optional[Entry] = None
cost_entry: Optional[Entry] = None
surcharge_entry: Optional[Entry] = None
payment_entry: Optional[Entry] = None

status_shipment_id_entry: Optional[Entry] = None
status_entry: Optional[Entry] = None

reg_username_entry: Optional[Entry] = None
reg_password_entry: Optional[Entry] = None
reg_role_entry: Optional[Entry] = None
reg_full_name_entry: Optional[Entry] = None
reg_email_entry: Optional[Entry] = None

login_root: Optional[Tk] = None
login_username_entry: Optional[Entry] = None
login_password_entry: Optional[Entry] = None

vehicle_reg_entry: Optional[Entry] = None
vehicle_type_entry: Optional[Entry] = None
vehicle_capacity_entry: Optional[Entry] = None
vehicle_maintenance_entry: Optional[Entry] = None
vehicle_status_entry: Optional[Entry] = None
vehicle_warehouse_entry: Optional[Entry] = None

driver_name_entry: Optional[Entry] = None
driver_phone_entry: Optional[Entry] = None
driver_license_entry: Optional[Entry] = None
driver_expiry_entry: Optional[Entry] = None
driver_notes_entry: Optional[Entry] = None
driver_shift_entry: Optional[Entry] = None

inventory_name_entry: Optional[Entry] = None
inventory_desc_entry: Optional[Entry] = None
inventory_category_entry: Optional[Entry] = None
inventory_price_entry: Optional[Entry] = None

warehouse_inventory_warehouse_entry: Optional[Entry] = None
warehouse_inventory_item_entry: Optional[Entry] = None
warehouse_inventory_quantity_entry: Optional[Entry] = None
warehouse_inventory_reorder_entry: Optional[Entry] = None
warehouse_inventory_location_entry: Optional[Entry] = None

assignment_shipment_entry: Optional[Entry] = None
assignment_driver_entry: Optional[Entry] = None
assignment_vehicle_entry: Optional[Entry] = None
assignment_route_entry: Optional[Entry] = None
assignment_date_entry: Optional[Entry] = None
assignment_dispatch_entry: Optional[Entry] = None
assignment_arrival_entry: Optional[Entry] = None
assignment_status_entry: Optional[Entry] = None

incident_shipment_entry: Optional[Entry] = None
incident_type_entry: Optional[Entry] = None
incident_desc_entry: Optional[Entry] = None
incident_status_entry: Optional[Entry] = None


def submit_customer():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager", "warehouse_staff"])

        add_customer(
            customer_name_entry.get(),
            customer_phone_entry.get(),
            customer_email_entry.get(),
            customer_address_entry.get(),
            user_id=current_user["user_id"]
        )
        messagebox.showinfo("Success", "Customer added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def submit_warehouse():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager"])

        add_warehouse(
            warehouse_name_entry.get(),
            warehouse_city_entry.get(),
            warehouse_address_entry.get(),
            warehouse_manager_entry.get(),
            user_id=current_user["user_id"]
        )
        messagebox.showinfo("Success", "Warehouse added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def submit_shipment():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager", "warehouse_staff"])

        add_shipment(
            order_entry.get(),
            int(sender_entry.get()),
            int(receiver_entry.get()),
            item_entry.get(),
            int(warehouse_entry.get()),
            address_entry.get(),
            float(cost_entry.get()),
            float(surcharge_entry.get()),
            payment_entry.get(),
            user_id=current_user["user_id"]
        )
        messagebox.showinfo("Success", "Shipment added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def submit_vehicle():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager"])

        add_vehicle(
            vehicle_reg_entry.get(),
            vehicle_type_entry.get(),
            float(vehicle_capacity_entry.get()),
            vehicle_maintenance_entry.get(),
            vehicle_status_entry.get(),
            int(vehicle_warehouse_entry.get()),
            user_id=current_user["user_id"]
        )

        messagebox.showinfo("Success", "Vehicle added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def submit_driver():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager"])

        add_driver(
            driver_name_entry.get(),
            driver_phone_entry.get(),
            driver_license_entry.get(),
            driver_expiry_entry.get(),
            driver_notes_entry.get(),
            driver_shift_entry.get(),
            user_id=current_user["user_id"]
        )

        messagebox.showinfo("Success", "Driver added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def submit_inventory_item():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager", "warehouse_staff"])

        add_inventory_item(
            inventory_name_entry.get(),
            inventory_desc_entry.get(),
            inventory_category_entry.get(),
            float(inventory_price_entry.get()),
            user_id=current_user["user_id"]
        )

        messagebox.showinfo("Success", "Inventory item added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def submit_warehouse_inventory():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager", "warehouse_staff"])

        add_warehouse_inventory(
            int(warehouse_inventory_warehouse_entry.get()),
            int(warehouse_inventory_item_entry.get()),
            int(warehouse_inventory_quantity_entry.get()),
            int(warehouse_inventory_reorder_entry.get()),
            warehouse_inventory_location_entry.get(),
            recorded_by_user_id=current_user["user_id"]
        )

        messagebox.showinfo("Success", "Warehouse inventory added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def submit_delivery_assignment():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager"])

        assign_delivery(
            int(assignment_shipment_entry.get()),
            int(assignment_driver_entry.get()),
            int(assignment_vehicle_entry.get()),
            assignment_route_entry.get(),
            assignment_date_entry.get(),
            assignment_dispatch_entry.get(),
            assignment_arrival_entry.get(),
            assignment_status_entry.get(),
            user_id=current_user["user_id"]
        )

        messagebox.showinfo("Success", "Delivery assigned successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def submit_incident():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager", "warehouse_staff", "driver"])

        add_incident(
            int(incident_shipment_entry.get()),
            incident_type_entry.get(),
            incident_desc_entry.get(),
            current_user["user_id"],
            incident_status_entry.get()
        )

        messagebox.showinfo("Success", "Incident recorded successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def change_status():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager", "warehouse_staff", "driver"])

        update_shipment_status(
            int(status_shipment_id_entry.get()),
            status_entry.get(),
            user_id=current_user["user_id"]
        )
        messagebox.showinfo("Success", "Shipment status updated.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_shipments():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = get_all_shipments()
        output_box.delete("1.0", tk.END)

        if not records:
            output_box.insert(tk.END, "No shipments found.\n")
            return

        for row in records:
            output_box.insert(
                tk.END,
                f"Shipment ID: {row[0]} | Order: {row[1]} | Sender ID: {row[2]} | Receiver ID: {row[3]} | "
                f"Item: {row[4]} | Warehouse ID: {row[5]} | Date: {row[6]} | "
                f"Status: {row[7]} | Cost: {row[8]} | Surcharge: {row[9]} | Payment: {row[10]}\n"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_customers():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = get_all_customers()
        output_box.delete("1.0", tk.END)

        if not records:
            output_box.insert(tk.END, "No customers found.\n")
            return

        for row in records:
            output_box.insert(
                tk.END,
                f"Customer ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | Email: {row[3]}\n"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_warehouses():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = get_all_warehouses()
        output_box.delete("1.0", tk.END)

        if not records:
            output_box.insert(tk.END, "No warehouses found.\n")
            return

        for row in records:
            output_box.insert(
                tk.END,
                f"Warehouse ID: {row[0]} | Name: {row[1]} | City: {row[2]} | Address: {row[3]} | Manager: {row[4]}\n"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_users():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")
        if output_box is None:
            raise ValueError("Output box is not ready.")

        require_role(current_user, ["admin"])

        records = get_all_users()
        output_box.delete("1.0", tk.END)

        if not records:
            output_box.insert(tk.END, "No users found.\n")
            return

        for row in records:
            output_box.insert(
                tk.END,
                f"User ID: {row[0]} | Username: {row[1]} | Name: {row[2]} | Email: {row[3]} | Role: {row[4]} | Active: {row[5]}\n"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_vehicles():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = get_all_vehicles()
        output_box.delete("1.0", tk.END)

        if not records:
            output_box.insert(tk.END, "No vehicles found.\n")
            return

        for row in records:
            output_box.insert(
                tk.END,
                f"Vehicle ID: {row[0]} | Reg: {row[1]} | Type: {row[2]} | "
                f"Capacity: {row[3]} | Maintenance Due: {row[4]} | "
                f"Status: {row[5]} | Warehouse ID: {row[6]}\n"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_drivers():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = get_all_drivers()
        output_box.delete("1.0", tk.END)

        if not records:
            output_box.insert(tk.END, "No drivers found.\n")
            return

        for row in records:
            output_box.insert(
                tk.END,
                f"Driver ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | "
                f"Licence: {row[3]} | Expiry: {row[4]} | Shift: {row[5]}\n"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_inventory():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = get_inventory_by_warehouse()
        output_box.delete("1.0", tk.END)

        if not records:
            output_box.insert(tk.END, "No inventory records found.\n")
            return

        for row in records:
            output_box.insert(
                tk.END,
                f"Record ID: {row[0]} | Warehouse: {row[1]} | Item: {row[2]} | "
                f"Quantity: {row[3]} | Reorder Level: {row[4]} | Location: {row[5]}\n"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_delivery_assignments():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = get_all_delivery_assignments()
        output_box.delete("1.0", tk.END)

        if not records:
            output_box.insert(tk.END, "No delivery assignments found.\n")
            return

        for row in records:
            output_box.insert(
                tk.END,
                f"Assignment ID: {row[0]} | Shipment ID: {row[1]} | Driver ID: {row[2]} | "
                f"Vehicle ID: {row[3]} | Route: {row[4]} | Date: {row[5]} | "
                f"Dispatch: {row[6]} | Arrival: {row[7]} | Status: {row[8]}\n"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_incidents():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = get_all_incidents()
        output_box.delete("1.0", tk.END)

        if not records:
            output_box.insert(tk.END, "No incidents found.\n")
            return

        for row in records:
            output_box.insert(
                tk.END,
                f"Incident ID: {row[0]} | Shipment ID: {row[1]} | Type: {row[2]} | "
                f"Description: {row[3]} | Reported By: {row[4]} | "
                f"Date: {row[5]} | Status: {row[6]}\n"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_shipment_status_report():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = get_shipment_status_report()
        output_box.delete("1.0", tk.END)

        if not records:
            output_box.insert(tk.END, "No shipment status report data found.\n")
            return

        output_box.insert(tk.END, "Shipment Status Report\n")
        output_box.insert(tk.END, "-" * 50 + "\n")
        for row in records:
            output_box.insert(tk.END, f"Status: {row[0]} | Count: {row[1]}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_vehicle_utilisation_report():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = get_vehicle_utilisation_report()
        output_box.delete("1.0", tk.END)

        if not records:
            output_box.insert(tk.END, "No vehicle utilisation data found.\n")
            return

        output_box.insert(tk.END, "Vehicle Utilisation Report\n")
        output_box.insert(tk.END, "-" * 50 + "\n")
        for row in records:
            output_box.insert(tk.END, f"Vehicle: {row[0]} | Assignments: {row[1]}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_warehouse_activity_report():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = get_warehouse_activity_report()
        output_box.delete("1.0", tk.END)

        if not records:
            output_box.insert(tk.END, "No warehouse activity data found.\n")
            return

        output_box.insert(tk.END, "Warehouse Activity Report\n")
        output_box.insert(tk.END, "-" * 50 + "\n")
        for row in records:
            output_box.insert(
                tk.END,
                f"Warehouse: {row[0]} | Activity: {row[1]} | Quantity: {row[2]} | Date: {row[3]}\n"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))

def register_new_user():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")
        if reg_username_entry is None or reg_password_entry is None or reg_role_entry is None:
            raise ValueError("Registration form is not ready.")
        if reg_full_name_entry is None or reg_email_entry is None:
            raise ValueError("Registration form is not ready.")

        require_role(current_user, ["admin"])

        register_user(
            reg_username_entry.get(),
            reg_password_entry.get(),
            reg_role_entry.get(),
            reg_full_name_entry.get(),
            reg_email_entry.get(),
            user_id=current_user["user_id"]
        )
        messagebox.showinfo("Success", "User registered successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def open_main_window():
    global output_box
    global customer_name_entry, customer_phone_entry, customer_email_entry, customer_address_entry
    global warehouse_name_entry, warehouse_city_entry, warehouse_address_entry, warehouse_manager_entry
    global order_entry, sender_entry, receiver_entry, item_entry, warehouse_entry, address_entry
    global cost_entry, surcharge_entry, payment_entry
    global status_shipment_id_entry, status_entry
    global reg_username_entry, reg_password_entry, reg_role_entry, reg_full_name_entry, reg_email_entry
    global vehicle_reg_entry, vehicle_type_entry, vehicle_capacity_entry
    global vehicle_maintenance_entry, vehicle_status_entry, vehicle_warehouse_entry
    global driver_name_entry, driver_phone_entry, driver_license_entry
    global driver_expiry_entry, driver_notes_entry, driver_shift_entry
    global inventory_name_entry, inventory_desc_entry, inventory_category_entry, inventory_price_entry
    global warehouse_inventory_warehouse_entry, warehouse_inventory_item_entry
    global warehouse_inventory_quantity_entry, warehouse_inventory_reorder_entry
    global warehouse_inventory_location_entry
    global assignment_shipment_entry, assignment_driver_entry, assignment_vehicle_entry
    global assignment_route_entry, assignment_date_entry, assignment_dispatch_entry
    global assignment_arrival_entry, assignment_status_entry
    global incident_shipment_entry, incident_type_entry, incident_desc_entry, incident_status_entry

    if current_user is None:
        raise ValueError("No user is currently logged in.")

    if login_root is not None:
        login_root.destroy()

    root = tk.Tk()
    root.title("Northshore Logistics System")
    root.geometry("1100x1100")

    title = tk.Label(root, text="Northshore Logistics Database System", font=("Arial", 16, "bold"))
    title.pack(pady=10)

    user_info_label = tk.Label(
        root,
        text=f"Logged in as: {current_user['full_name']} ({current_user['role_name']})",
        font=("Arial", 11, "italic")
    )
    user_info_label.pack(pady=5)

    customer_frame = tk.LabelFrame(root, text="Add Customer", padx=10, pady=10)
    customer_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(customer_frame, text="Name").grid(row=0, column=0)
    customer_name_entry = tk.Entry(customer_frame)
    customer_name_entry.grid(row=0, column=1)

    tk.Label(customer_frame, text="Phone").grid(row=1, column=0)
    customer_phone_entry = tk.Entry(customer_frame)
    customer_phone_entry.grid(row=1, column=1)

    tk.Label(customer_frame, text="Email").grid(row=2, column=0)
    customer_email_entry = tk.Entry(customer_frame)
    customer_email_entry.grid(row=2, column=1)

    tk.Label(customer_frame, text="Address").grid(row=3, column=0)
    customer_address_entry = tk.Entry(customer_frame, width=40)
    customer_address_entry.grid(row=3, column=1)

    tk.Button(customer_frame, text="Add Customer", command=submit_customer).grid(row=4, column=0, columnspan=2, pady=5)

    warehouse_frame = tk.LabelFrame(root, text="Add Warehouse", padx=10, pady=10)
    warehouse_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(warehouse_frame, text="Warehouse Name").grid(row=0, column=0)
    warehouse_name_entry = tk.Entry(warehouse_frame)
    warehouse_name_entry.grid(row=0, column=1)

    tk.Label(warehouse_frame, text="City").grid(row=1, column=0)
    warehouse_city_entry = tk.Entry(warehouse_frame)
    warehouse_city_entry.grid(row=1, column=1)

    tk.Label(warehouse_frame, text="Address").grid(row=2, column=0)
    warehouse_address_entry = tk.Entry(warehouse_frame, width=40)
    warehouse_address_entry.grid(row=2, column=1)

    tk.Label(warehouse_frame, text="Manager Name").grid(row=3, column=0)
    warehouse_manager_entry = tk.Entry(warehouse_frame)
    warehouse_manager_entry.grid(row=3, column=1)

    tk.Button(warehouse_frame, text="Add Warehouse", command=submit_warehouse).grid(row=4, column=0, columnspan=2, pady=5)

    shipment_frame = tk.LabelFrame(root, text="Add Shipment", padx=10, pady=10)
    shipment_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(shipment_frame, text="Order Number").grid(row=0, column=0)
    order_entry = tk.Entry(shipment_frame)
    order_entry.grid(row=0, column=1)

    tk.Label(shipment_frame, text="Sender Customer ID").grid(row=1, column=0)
    sender_entry = tk.Entry(shipment_frame)
    sender_entry.grid(row=1, column=1)

    tk.Label(shipment_frame, text="Receiver Customer ID").grid(row=2, column=0)
    receiver_entry = tk.Entry(shipment_frame)
    receiver_entry.grid(row=2, column=1)

    tk.Label(shipment_frame, text="Item Description").grid(row=3, column=0)
    item_entry = tk.Entry(shipment_frame)
    item_entry.grid(row=3, column=1)

    tk.Label(shipment_frame, text="Origin Warehouse ID").grid(row=4, column=0)
    warehouse_entry = tk.Entry(shipment_frame)
    warehouse_entry.grid(row=4, column=1)

    tk.Label(shipment_frame, text="Destination Address").grid(row=5, column=0)
    address_entry = tk.Entry(shipment_frame, width=40)
    address_entry.grid(row=5, column=1)

    tk.Label(shipment_frame, text="Transport Cost").grid(row=6, column=0)
    cost_entry = tk.Entry(shipment_frame)
    cost_entry.grid(row=6, column=1)

    tk.Label(shipment_frame, text="Surcharge").grid(row=7, column=0)
    surcharge_entry = tk.Entry(shipment_frame)
    surcharge_entry.grid(row=7, column=1)

    tk.Label(shipment_frame, text="Payment Status").grid(row=8, column=0)
    payment_entry = tk.Entry(shipment_frame)
    payment_entry.grid(row=8, column=1)

    tk.Button(shipment_frame, text="Add Shipment", command=submit_shipment).grid(row=9, column=0, columnspan=2, pady=5)

    status_frame = tk.LabelFrame(root, text="Update Shipment Status", padx=10, pady=10)
    status_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(status_frame, text="Shipment ID").grid(row=0, column=0)
    status_shipment_id_entry = tk.Entry(status_frame)
    status_shipment_id_entry.grid(row=0, column=1)

    tk.Label(status_frame, text="New Status").grid(row=1, column=0)
    status_entry = tk.Entry(status_frame)
    status_entry.grid(row=1, column=1)

    tk.Button(status_frame, text="Update Status", command=change_status).grid(row=2, column=0, columnspan=2, pady=5)

    vehicle_frame = tk.LabelFrame(root, text="Add Vehicle", padx=10, pady=10)
    vehicle_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(vehicle_frame, text="Registration Number").grid(row=0, column=0)
    vehicle_reg_entry = tk.Entry(vehicle_frame)
    vehicle_reg_entry.grid(row=0, column=1)

    tk.Label(vehicle_frame, text="Vehicle Type").grid(row=1, column=0)
    vehicle_type_entry = tk.Entry(vehicle_frame)
    vehicle_type_entry.grid(row=1, column=1)

    tk.Label(vehicle_frame, text="Capacity").grid(row=2, column=0)
    vehicle_capacity_entry = tk.Entry(vehicle_frame)
    vehicle_capacity_entry.grid(row=2, column=1)

    tk.Label(vehicle_frame, text="Maintenance Due Date").grid(row=3, column=0)
    vehicle_maintenance_entry = tk.Entry(vehicle_frame)
    vehicle_maintenance_entry.grid(row=3, column=1)

    tk.Label(vehicle_frame, text="Availability Status").grid(row=4, column=0)
    vehicle_status_entry = tk.Entry(vehicle_frame)
    vehicle_status_entry.grid(row=4, column=1)

    tk.Label(vehicle_frame, text="Assigned Warehouse ID").grid(row=5, column=0)
    vehicle_warehouse_entry = tk.Entry(vehicle_frame)
    vehicle_warehouse_entry.grid(row=5, column=1)

    tk.Button(vehicle_frame, text="Add Vehicle", command=submit_vehicle).grid(row=6, column=0, columnspan=2, pady=5)

    driver_frame = tk.LabelFrame(root, text="Add Driver", padx=10, pady=10)
    driver_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(driver_frame, text="Full Name").grid(row=0, column=0)
    driver_name_entry = tk.Entry(driver_frame)
    driver_name_entry.grid(row=0, column=1)

    tk.Label(driver_frame, text="Phone").grid(row=1, column=0)
    driver_phone_entry = tk.Entry(driver_frame)
    driver_phone_entry.grid(row=1, column=1)

    tk.Label(driver_frame, text="Licence Number").grid(row=2, column=0)
    driver_license_entry = tk.Entry(driver_frame)
    driver_license_entry.grid(row=2, column=1)

    tk.Label(driver_frame, text="Licence Expiry").grid(row=3, column=0)
    driver_expiry_entry = tk.Entry(driver_frame)
    driver_expiry_entry.grid(row=3, column=1)

    tk.Label(driver_frame, text="Route History Notes").grid(row=4, column=0)
    driver_notes_entry = tk.Entry(driver_frame, width=40)
    driver_notes_entry.grid(row=4, column=1)

    tk.Label(driver_frame, text="Shift Assignment").grid(row=5, column=0)
    driver_shift_entry = tk.Entry(driver_frame)
    driver_shift_entry.grid(row=5, column=1)

    tk.Button(driver_frame, text="Add Driver", command=submit_driver).grid(row=6, column=0, columnspan=2, pady=5)

    inventory_frame = tk.LabelFrame(root, text="Add Inventory Item", padx=10, pady=10)
    inventory_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(inventory_frame, text="Item Name").grid(row=0, column=0)
    inventory_name_entry = tk.Entry(inventory_frame)
    inventory_name_entry.grid(row=0, column=1)

    tk.Label(inventory_frame, text="Description").grid(row=1, column=0)
    inventory_desc_entry = tk.Entry(inventory_frame, width=40)
    inventory_desc_entry.grid(row=1, column=1)

    tk.Label(inventory_frame, text="Category").grid(row=2, column=0)
    inventory_category_entry = tk.Entry(inventory_frame)
    inventory_category_entry.grid(row=2, column=1)

    tk.Label(inventory_frame, text="Unit Price").grid(row=3, column=0)
    inventory_price_entry = tk.Entry(inventory_frame)
    inventory_price_entry.grid(row=3, column=1)

    tk.Button(inventory_frame, text="Add Inventory Item", command=submit_inventory_item).grid(row=4, column=0,
                                                                                              columnspan=2, pady=5)

    warehouse_inventory_frame = tk.LabelFrame(root, text="Add Warehouse Inventory", padx=10, pady=10)
    warehouse_inventory_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(warehouse_inventory_frame, text="Warehouse ID").grid(row=0, column=0)
    warehouse_inventory_warehouse_entry = tk.Entry(warehouse_inventory_frame)
    warehouse_inventory_warehouse_entry.grid(row=0, column=1)

    tk.Label(warehouse_inventory_frame, text="Item ID").grid(row=1, column=0)
    warehouse_inventory_item_entry = tk.Entry(warehouse_inventory_frame)
    warehouse_inventory_item_entry.grid(row=1, column=1)

    tk.Label(warehouse_inventory_frame, text="Quantity").grid(row=2, column=0)
    warehouse_inventory_quantity_entry = tk.Entry(warehouse_inventory_frame)
    warehouse_inventory_quantity_entry.grid(row=2, column=1)

    tk.Label(warehouse_inventory_frame, text="Reorder Level").grid(row=3, column=0)
    warehouse_inventory_reorder_entry = tk.Entry(warehouse_inventory_frame)
    warehouse_inventory_reorder_entry.grid(row=3, column=1)

    tk.Label(warehouse_inventory_frame, text="Item Location").grid(row=4, column=0)
    warehouse_inventory_location_entry = tk.Entry(warehouse_inventory_frame)
    warehouse_inventory_location_entry.grid(row=4, column=1)

    tk.Button(warehouse_inventory_frame, text="Add Warehouse Inventory", command=submit_warehouse_inventory).grid(row=5,
                                                                                                                  column=0,
                                                                                                                  columnspan=2,
                                                                                                                  pady=5)
    assignment_frame = tk.LabelFrame(root, text="Assign Delivery", padx=10, pady=10)
    assignment_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(assignment_frame, text="Shipment ID").grid(row=0, column=0)
    assignment_shipment_entry = tk.Entry(assignment_frame)
    assignment_shipment_entry.grid(row=0, column=1)

    tk.Label(assignment_frame, text="Driver ID").grid(row=1, column=0)
    assignment_driver_entry = tk.Entry(assignment_frame)
    assignment_driver_entry.grid(row=1, column=1)

    tk.Label(assignment_frame, text="Vehicle ID").grid(row=2, column=0)
    assignment_vehicle_entry = tk.Entry(assignment_frame)
    assignment_vehicle_entry.grid(row=2, column=1)

    tk.Label(assignment_frame, text="Route Details").grid(row=3, column=0)
    assignment_route_entry = tk.Entry(assignment_frame, width=40)
    assignment_route_entry.grid(row=3, column=1)

    tk.Label(assignment_frame, text="Delivery Date").grid(row=4, column=0)
    assignment_date_entry = tk.Entry(assignment_frame)
    assignment_date_entry.grid(row=4, column=1)

    tk.Label(assignment_frame, text="Dispatch Time").grid(row=5, column=0)
    assignment_dispatch_entry = tk.Entry(assignment_frame)
    assignment_dispatch_entry.grid(row=5, column=1)

    tk.Label(assignment_frame, text="Arrival Time").grid(row=6, column=0)
    assignment_arrival_entry = tk.Entry(assignment_frame)
    assignment_arrival_entry.grid(row=6, column=1)

    tk.Label(assignment_frame, text="Assignment Status").grid(row=7, column=0)
    assignment_status_entry = tk.Entry(assignment_frame)
    assignment_status_entry.grid(row=7, column=1)

    tk.Button(assignment_frame, text="Assign Delivery", command=submit_delivery_assignment).grid(row=8, column=0,
                                                                                                 columnspan=2, pady=5)

    incident_frame = tk.LabelFrame(root, text="Record Incident", padx=10, pady=10)
    incident_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(incident_frame, text="Shipment ID").grid(row=0, column=0)
    incident_shipment_entry = tk.Entry(incident_frame)
    incident_shipment_entry.grid(row=0, column=1)

    tk.Label(incident_frame, text="Incident Type").grid(row=1, column=0)
    incident_type_entry = tk.Entry(incident_frame)
    incident_type_entry.grid(row=1, column=1)

    tk.Label(incident_frame, text="Description").grid(row=2, column=0)
    incident_desc_entry = tk.Entry(incident_frame, width=40)
    incident_desc_entry.grid(row=2, column=1)

    tk.Label(incident_frame, text="Resolution Status").grid(row=3, column=0)
    incident_status_entry = tk.Entry(incident_frame)
    incident_status_entry.grid(row=3, column=1)

    tk.Button(incident_frame, text="Record Incident", command=submit_incident).grid(row=4, column=0, columnspan=2,
                                                                                    pady=5)

    if has_role(current_user, ["admin"]):
        users_frame = tk.LabelFrame(root, text="Register New User (Admin Only)", padx=10, pady=10)
        users_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(users_frame, text="Username").grid(row=0, column=0)
        reg_username_entry = tk.Entry(users_frame)
        reg_username_entry.grid(row=0, column=1)

        tk.Label(users_frame, text="Password").grid(row=1, column=0)
        reg_password_entry = tk.Entry(users_frame, show="*")
        reg_password_entry.grid(row=1, column=1)

        tk.Label(users_frame, text="Role").grid(row=2, column=0)
        reg_role_entry = tk.Entry(users_frame)
        reg_role_entry.grid(row=2, column=1)

        tk.Label(users_frame, text="Full Name").grid(row=3, column=0)
        reg_full_name_entry = tk.Entry(users_frame)
        reg_full_name_entry.grid(row=3, column=1)

        tk.Label(users_frame, text="Email").grid(row=4, column=0)
        reg_email_entry = tk.Entry(users_frame)
        reg_email_entry.grid(row=4, column=1)

        tk.Button(users_frame, text="Register User", command=register_new_user).grid(row=5, column=0, columnspan=2, pady=5)

    output_frame = tk.LabelFrame(root, text="System Output", padx=10, pady=10)
    output_frame.pack(fill="both", expand=True, padx=10, pady=5)

    tk.Button(output_frame, text="Show All Customers", command=show_customers).pack(pady=5)
    tk.Button(output_frame, text="Show All Warehouses", command=show_warehouses).pack(pady=5)
    tk.Button(output_frame, text="Show All Shipments", command=show_shipments).pack(pady=5)
    tk.Button(output_frame, text="Show All Vehicles", command=show_vehicles).pack(pady=5)
    tk.Button(output_frame, text="Show All Drivers", command=show_drivers).pack(pady=5)
    tk.Button(output_frame, text="Show Inventory by Warehouse", command=show_inventory).pack(pady=5)
    tk.Button(output_frame, text="Show Delivery Assignments", command=show_delivery_assignments).pack(pady=5)
    tk.Button(output_frame, text="Show Incidents", command=show_incidents).pack(pady=5)

    tk.Button(output_frame, text="Shipment Status Report", command=show_shipment_status_report).pack(pady=5)
    tk.Button(output_frame, text="Vehicle Utilisation Report", command=show_vehicle_utilisation_report).pack(pady=5)
    tk.Button(output_frame, text="Warehouse Activity Report", command=show_warehouse_activity_report).pack(pady=5)


    if has_role(current_user, ["admin"]):
        tk.Button(output_frame, text="Show All Users", command=show_users).pack(pady=5)

    output_box = tk.Text(output_frame, height=15, width=120)
    output_box.pack()

    root.mainloop()


def attempt_login():
    global current_user
    try:
        if login_username_entry is None or login_password_entry is None:
            raise ValueError("Login form is not ready.")

        current_user = login_user(login_username_entry.get(), login_password_entry.get())
        messagebox.showinfo("Success", f"Welcome, {current_user['full_name']}!")
        open_main_window()
    except Exception as e:
        messagebox.showerror("Login Failed", str(e))


login_root = tk.Tk()
login_root.title("Login - Northshore Logistics System")
login_root.geometry("400x250")

tk.Label(login_root, text="Northshore Logistics Login", font=("Arial", 14, "bold")).pack(pady=15)

login_frame = tk.Frame(login_root)
login_frame.pack(pady=10)

tk.Label(login_frame, text="Username").grid(row=0, column=0, padx=5, pady=5)
login_username_entry = tk.Entry(login_frame)
login_username_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(login_frame, text="Password").grid(row=1, column=0, padx=5, pady=5)
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(login_root, text="Login", command=attempt_login).pack(pady=15)

login_root.mainloop()