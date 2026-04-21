import tkinter as tk
from tkinter import messagebox
from typing import Optional
from tkinter import Entry, Text, Tk
from tkinter import ttk
from tkinter.ttk import Combobox

from services.auth_service import login_user, register_user, get_all_users
from services.customer_service import add_customer, get_all_customers
from services.warehouse_service import add_warehouse, get_all_warehouses
from services.vehicle_service import add_vehicle, get_all_vehicles, update_vehicle
from services.driver_service import add_driver, get_all_drivers
from services.inventory_service import add_inventory_item, add_warehouse_inventory, get_inventory_by_warehouse, update_inventory_quantity
from services.delivery_service import (
    assign_delivery,
    get_all_delivery_assignments,
    update_delivery_assignment
)
from services.incident_service import add_incident, get_all_incidents

from services.reports_service import (
    get_shipment_status_report,
    get_vehicle_utilisation_report,
    get_warehouse_activity_report
)
from services.payment_service import add_payment, get_all_payments, update_payment_status
from services.shipment_service import (
    add_shipment,
    get_all_shipments,
    update_shipment_status,
    search_shipments_by_order,
    filter_shipments_by_status
)

from utils.access_control import has_role, require_role
from utils.security import simple_decrypt

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
status_shipment_id_entry: Optional[Entry] = None

payment_entry: Optional[Combobox] = None
status_entry: Optional[Combobox] = None
filter_status_entry: Optional[Combobox] = None

reg_username_entry: Optional[Entry] = None
reg_password_entry: Optional[Entry] = None
reg_role_entry: Optional[Combobox] = None
reg_full_name_entry: Optional[Entry] = None
reg_email_entry: Optional[Entry] = None

login_root: Optional[Tk] = None
login_username_entry: Optional[Entry] = None
login_password_entry: Optional[Entry] = None

vehicle_reg_entry: Optional[Entry] = None
vehicle_type_entry: Optional[Entry] = None
vehicle_capacity_entry: Optional[Entry] = None
vehicle_maintenance_entry: Optional[Entry] = None
vehicle_warehouse_entry: Optional[Entry] = None
vehicle_update_id_entry: Optional[Entry] = None
vehicle_update_type_entry: Optional[Entry] = None
vehicle_update_capacity_entry: Optional[Entry] = None
vehicle_update_maintenance_entry: Optional[Entry] = None
vehicle_update_warehouse_entry: Optional[Entry] = None

vehicle_status_entry: Optional[Combobox] = None
vehicle_update_status_entry: Optional[Combobox] = None

delivery_update_id_entry: Optional[Entry] = None
delivery_update_driver_entry: Optional[Entry] = None
delivery_update_vehicle_entry: Optional[Entry] = None
delivery_update_route_entry: Optional[Entry] = None
delivery_update_date_entry: Optional[Entry] = None
delivery_update_dispatch_entry: Optional[Entry] = None
delivery_update_arrival_entry: Optional[Entry] = None
delivery_update_status_entry: Optional[Combobox] = None

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
warehouse_inventory_update_entry: Optional[Entry] = None

assignment_shipment_entry: Optional[Entry] = None
assignment_driver_entry: Optional[Entry] = None
assignment_vehicle_entry: Optional[Entry] = None
assignment_route_entry: Optional[Entry] = None
assignment_date_entry: Optional[Entry] = None
assignment_dispatch_entry: Optional[Entry] = None
assignment_arrival_entry: Optional[Entry] = None
assignment_status_entry: Optional[Combobox] = None

incident_shipment_entry: Optional[Entry] = None
incident_type_entry: Optional[Entry] = None
incident_desc_entry: Optional[Entry] = None
incident_status_entry: Optional[Combobox] = None

payment_shipment_entry: Optional[Entry] = None
payment_amount_due_entry: Optional[Entry] = None
payment_amount_paid_entry: Optional[Entry] = None
payment_method_entry: Optional[Entry] = None
payment_date_entry: Optional[Entry] = None
payment_status_new_entry: Optional[Combobox] = None

payment_update_id_entry: Optional[Entry] = None
payment_update_status_entry: Optional[Combobox] = None

search_order_entry: Optional[Entry] = None



SHIPMENT_STATUS_OPTIONS = [
    "In Transit",
    "Delivered",
    "Delayed",
    "Returned to Warehouse",
    "Failed Delivery"
]

PAYMENT_STATUS_OPTIONS = [
    "Pending",
    "Partially Paid",
    "Paid",
    "Overdue",
    "Cancelled"
]

VEHICLE_STATUS_OPTIONS = [
    "Available",
    "In Use",
    "Under Maintenance",
    "Out of Service"
]

ASSIGNMENT_STATUS_OPTIONS = [
    "Scheduled",
    "Dispatched",
    "In Progress",
    "Completed",
    "Cancelled"
]

INCIDENT_STATUS_OPTIONS = [
    "Open",
    "Investigating",
    "Resolved",
    "Closed"
]

ROLE_OPTIONS = [
    "admin",
    "manager",
    "warehouse_staff",
    "driver"
]


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

        sender_id = int(sender_entry.get().strip())
        receiver_id = int(receiver_entry.get().strip())
        warehouse_id = int(warehouse_entry.get().strip())
        transport_cost = float(cost_entry.get().strip())
        surcharge = float(surcharge_entry.get().strip())

        add_shipment(
            order_entry.get().strip(),
            sender_id,
            receiver_id,
            item_entry.get().strip(),
            warehouse_id,
            address_entry.get().strip(),
            transport_cost,
            surcharge,
            payment_entry.get().strip(),
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


def update_inventory_gui():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager", "warehouse_staff"])

        warehouse_id = int(warehouse_inventory_warehouse_entry.get())
        item_id = int(warehouse_inventory_item_entry.get())
        quantity_change = int(warehouse_inventory_update_entry.get())

        update_inventory_quantity(
            warehouse_id,
            item_id,
            quantity_change,
            user_id=current_user["user_id"]
        )

        messagebox.showinfo("Success", "Inventory updated successfully.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_vehicle_gui():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager"])

        update_vehicle(
            int(vehicle_update_id_entry.get()),
            vehicle_update_type_entry.get(),
            float(vehicle_update_capacity_entry.get()),
            vehicle_update_maintenance_entry.get(),
            vehicle_update_status_entry.get(),
            int(vehicle_update_warehouse_entry.get()),
            user_id=current_user["user_id"]
        )

        messagebox.showinfo("Success", "Vehicle updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_delivery_assignment_gui():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager"])

        update_delivery_assignment(
            int(delivery_update_id_entry.get()),
            int(delivery_update_driver_entry.get()),
            int(delivery_update_vehicle_entry.get()),
            delivery_update_route_entry.get(),
            delivery_update_date_entry.get(),
            delivery_update_dispatch_entry.get(),
            delivery_update_arrival_entry.get(),
            delivery_update_status_entry.get(),
            user_id=current_user["user_id"]
        )

        messagebox.showinfo("Success", "Delivery assignment updated successfully.")
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
        display_shipment_records(records)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_shipment_records(records):
    if output_box is None:
        raise ValueError("Output box is not ready.")

    output_box.delete("1.0", tk.END)

    if not records:
        output_box.insert(tk.END, "No shipments found.\n")
        return

    for row in records:
        output_box.insert(
            tk.END,
            f"Shipment ID: {row[0]} | Order: {row[1]} | Sender ID: {row[2]} | "
            f"Receiver ID: {row[3]} | Item: {row[4]} | Warehouse ID: {row[5]} | "
            f"Date: {row[6]} | Status: {row[7]} | Cost: {row[8]} | "
            f"Surcharge: {row[9]} | Payment: {row[10]}\n"
        )

def search_shipments():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = search_shipments_by_order(search_order_entry.get())
        display_shipment_records(records)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def filter_shipments():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = filter_shipments_by_status(filter_status_entry.get())
        display_shipment_records(records)
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
            decrypted_phone = simple_decrypt(row[2])
            decrypted_license = simple_decrypt(row[3])

            output_box.insert(
                tk.END,
                f"Driver ID: {row[0]} | Name: {row[1]} | Phone: {decrypted_phone} | "
                f"Licence: {decrypted_license} | Expiry: {row[4]} | Shift: {row[5]}\n"
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

def show_payments():
    try:
        if output_box is None:
            raise ValueError("Output box is not ready.")

        records = get_all_payments()
        output_box.delete("1.0", tk.END)

        if not records:
            output_box.insert(tk.END, "No payments found.\n")
            return

        for row in records:
            decrypted_method = simple_decrypt(row[4])
            output_box.insert(
                tk.END,
                f"Payment ID: {row[0]} | Shipment ID: {row[1]} | "
                f"Amount Due: {row[2]} | Amount Paid: {row[3]} | "
                f"Method: {decrypted_method} | Date: {row[5]} | Status: {row[6]}\n"
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

def submit_payment():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager", "warehouse_staff"])

        add_payment(
            int(payment_shipment_entry.get()),
            float(payment_amount_due_entry.get()),
            float(payment_amount_paid_entry.get()),
            payment_method_entry.get(),
            payment_date_entry.get(),
            payment_status_new_entry.get(),
            user_id=current_user["user_id"]
        )

        messagebox.showinfo("Success", "Payment added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def change_payment_status():
    global current_user
    try:
        if current_user is None:
            raise ValueError("No user is currently logged in.")

        require_role(current_user, ["admin", "manager"])

        update_payment_status(
            int(payment_update_id_entry.get()),
            payment_update_status_entry.get(),
            user_id=current_user["user_id"]
        )

        messagebox.showinfo("Success", "Payment status updated.")
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
    global warehouse_inventory_update_entry
    global assignment_shipment_entry, assignment_driver_entry, assignment_vehicle_entry
    global assignment_route_entry, assignment_date_entry, assignment_dispatch_entry
    global assignment_arrival_entry, assignment_status_entry
    global incident_shipment_entry, incident_type_entry, incident_desc_entry, incident_status_entry
    global payment_shipment_entry, payment_amount_due_entry, payment_amount_paid_entry
    global payment_method_entry, payment_date_entry, payment_status_new_entry
    global payment_update_id_entry, payment_update_status_entry
    global search_order_entry, filter_status_entry
    global vehicle_update_id_entry
    global vehicle_update_type_entry, vehicle_update_capacity_entry
    global vehicle_update_maintenance_entry, vehicle_update_status_entry
    global vehicle_update_warehouse_entry
    global delivery_update_id_entry, delivery_update_driver_entry, delivery_update_vehicle_entry
    global delivery_update_route_entry, delivery_update_date_entry
    global delivery_update_dispatch_entry, delivery_update_arrival_entry, delivery_update_status_entry

    if current_user is None:
        raise ValueError("No user is currently logged in.")

    if login_root is not None:
        login_root.destroy()

    root = tk.Tk()
    root.title("Northshore Logistics System")
    root.geometry("1200x950")

    title = tk.Label(
        root,
        text="Northshore Logistics Database System",
        font=("Arial", 16, "bold")
    )
    title.pack(pady=10)

    user_info_label = tk.Label(
        root,
        text=f"Logged in as: {current_user['full_name']} ({current_user['role_name']})",
        font=("Arial", 11, "italic")
    )
    user_info_label.pack(pady=5)

    # -------------------------
    # SCROLLABLE TOP AREA
    # -------------------------

    top_wrapper = tk.Frame(root)
    top_wrapper.pack(fill="both", expand=True, padx=10, pady=5)

    top_canvas = tk.Canvas(top_wrapper, height=500)
    top_scrollbar = tk.Scrollbar(top_wrapper, orient="vertical", command=top_canvas.yview)
    top_container = tk.Frame(top_canvas)

    top_container.bind(
        "<Configure>",
        lambda e: top_canvas.configure(scrollregion=top_canvas.bbox("all"))
    )

    top_window = top_canvas.create_window((0, 0), window=top_container, anchor="nw")

    def _resize_top_container(event):
        top_canvas.itemconfig(top_window, width=event.width)

    top_canvas.bind("<Configure>", _resize_top_container)

    def _on_mousewheel(event):
        top_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    top_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    top_canvas.configure(yscrollcommand=top_scrollbar.set)

    top_canvas.pack(side="left", fill="both", expand=True)
    top_scrollbar.pack(side="right", fill="y")

    # -------------------------
    # FIXED BOTTOM AREA
    # -------------------------

    bottom_container = tk.Frame(root)
    bottom_container.pack(fill="both", expand=True, padx=10, pady=5)

    # -------------------------
    # FORM SECTIONS
    # -------------------------

    customer_frame = tk.LabelFrame(top_container, text="Add Customer", padx=10, pady=10)
    customer_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(customer_frame, text="Name").grid(row=0, column=0, sticky="w")
    customer_name_entry = tk.Entry(customer_frame)
    customer_name_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(customer_frame, text="Phone").grid(row=1, column=0, sticky="w")
    customer_phone_entry = tk.Entry(customer_frame)
    customer_phone_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(customer_frame, text="Email").grid(row=2, column=0, sticky="w")
    customer_email_entry = tk.Entry(customer_frame)
    customer_email_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(customer_frame, text="Address").grid(row=3, column=0, sticky="w")
    customer_address_entry = tk.Entry(customer_frame, width=40)
    customer_address_entry.grid(row=3, column=1, padx=5, pady=2)

    tk.Button(customer_frame, text="Add Customer", command=submit_customer).grid(
        row=4, column=0, columnspan=2, pady=5
    )

    warehouse_frame = tk.LabelFrame(top_container, text="Add Warehouse", padx=10, pady=10)
    warehouse_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(warehouse_frame, text="Warehouse Name").grid(row=0, column=0, sticky="w")
    warehouse_name_entry = tk.Entry(warehouse_frame)
    warehouse_name_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(warehouse_frame, text="City").grid(row=1, column=0, sticky="w")
    warehouse_city_entry = tk.Entry(warehouse_frame)
    warehouse_city_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(warehouse_frame, text="Address").grid(row=2, column=0, sticky="w")
    warehouse_address_entry = tk.Entry(warehouse_frame, width=40)
    warehouse_address_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(warehouse_frame, text="Manager Name").grid(row=3, column=0, sticky="w")
    warehouse_manager_entry = tk.Entry(warehouse_frame)
    warehouse_manager_entry.grid(row=3, column=1, padx=5, pady=2)

    tk.Button(warehouse_frame, text="Add Warehouse", command=submit_warehouse).grid(
        row=4, column=0, columnspan=2, pady=5
    )

    shipment_frame = tk.LabelFrame(top_container, text="Add Shipment", padx=10, pady=10)
    shipment_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(shipment_frame, text="Order Number").grid(row=0, column=0, sticky="w")
    order_entry = tk.Entry(shipment_frame)
    order_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(shipment_frame, text="Sender Customer ID").grid(row=1, column=0, sticky="w")
    sender_entry = tk.Entry(shipment_frame)
    sender_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(shipment_frame, text="Receiver Customer ID").grid(row=2, column=0, sticky="w")
    receiver_entry = tk.Entry(shipment_frame)
    receiver_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(shipment_frame, text="Item Description").grid(row=3, column=0, sticky="w")
    item_entry = tk.Entry(shipment_frame)
    item_entry.grid(row=3, column=1, padx=5, pady=2)

    tk.Label(shipment_frame, text="Origin Warehouse ID").grid(row=4, column=0, sticky="w")
    warehouse_entry = tk.Entry(shipment_frame)
    warehouse_entry.grid(row=4, column=1, padx=5, pady=2)

    tk.Label(shipment_frame, text="Destination Address").grid(row=5, column=0, sticky="w")
    address_entry = tk.Entry(shipment_frame, width=40)
    address_entry.grid(row=5, column=1, padx=5, pady=2)

    tk.Label(shipment_frame, text="Transport Cost").grid(row=6, column=0, sticky="w")
    cost_entry = tk.Entry(shipment_frame)
    cost_entry.grid(row=6, column=1, padx=5, pady=2)

    tk.Label(shipment_frame, text="Surcharge").grid(row=7, column=0, sticky="w")
    surcharge_entry = tk.Entry(shipment_frame)
    surcharge_entry.grid(row=7, column=1, padx=5, pady=2)

    tk.Label(shipment_frame, text="Payment Status").grid(row=8, column=0, sticky="w")
    payment_entry = ttk.Combobox(shipment_frame, values=PAYMENT_STATUS_OPTIONS, state="readonly")
    payment_entry.grid(row=8, column=1, padx=5, pady=2)
    payment_entry.set(PAYMENT_STATUS_OPTIONS[0])

    tk.Button(shipment_frame, text="Add Shipment", command=submit_shipment).grid(
        row=9, column=0, columnspan=2, pady=5
    )

    status_frame = tk.LabelFrame(top_container, text="Update Shipment Status", padx=10, pady=10)
    status_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(status_frame, text="Shipment ID").grid(row=0, column=0, sticky="w")
    status_shipment_id_entry = tk.Entry(status_frame)
    status_shipment_id_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(status_frame, text="New Status").grid(row=1, column=0, sticky="w")
    status_entry = ttk.Combobox(status_frame, values=SHIPMENT_STATUS_OPTIONS, state="readonly")
    status_entry.grid(row=1, column=1, padx=5, pady=2)
    status_entry.set(SHIPMENT_STATUS_OPTIONS[0])

    tk.Button(status_frame, text="Update Status", command=change_status).grid(
        row=2, column=0, columnspan=2, pady=5
    )

    vehicle_frame = tk.LabelFrame(top_container, text="Add Vehicle", padx=10, pady=10)
    vehicle_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(vehicle_frame, text="Registration Number").grid(row=0, column=0, sticky="w")
    vehicle_reg_entry = tk.Entry(vehicle_frame)
    vehicle_reg_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(vehicle_frame, text="Vehicle Type").grid(row=1, column=0, sticky="w")
    vehicle_type_entry = tk.Entry(vehicle_frame)
    vehicle_type_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(vehicle_frame, text="Capacity").grid(row=2, column=0, sticky="w")
    vehicle_capacity_entry = tk.Entry(vehicle_frame)
    vehicle_capacity_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(vehicle_frame, text="Maintenance Due Date").grid(row=3, column=0, sticky="w")
    vehicle_maintenance_entry = tk.Entry(vehicle_frame)
    vehicle_maintenance_entry.grid(row=3, column=1, padx=5, pady=2)

    tk.Label(vehicle_frame, text="Availability Status").grid(row=4, column=0, sticky="w")
    vehicle_status_entry = ttk.Combobox(vehicle_frame, values=VEHICLE_STATUS_OPTIONS, state="readonly")
    vehicle_status_entry.grid(row=4, column=1, padx=5, pady=2)
    vehicle_status_entry.set(VEHICLE_STATUS_OPTIONS[0])

    tk.Label(vehicle_frame, text="Assigned Warehouse ID").grid(row=5, column=0, sticky="w")
    vehicle_warehouse_entry = tk.Entry(vehicle_frame)
    vehicle_warehouse_entry.grid(row=5, column=1, padx=5, pady=2)

    tk.Button(vehicle_frame, text="Add Vehicle", command=submit_vehicle).grid(
        row=6, column=0, columnspan=2, pady=5
    )

    vehicle_update_frame = tk.LabelFrame(top_container, text="Update Vehicle", padx=10, pady=10)
    vehicle_update_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(vehicle_update_frame, text="Vehicle ID").grid(row=0, column=0, sticky="w")
    vehicle_update_id_entry = tk.Entry(vehicle_update_frame)
    vehicle_update_id_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(vehicle_update_frame, text="Vehicle Type").grid(row=1, column=0, sticky="w")
    vehicle_update_type_entry = tk.Entry(vehicle_update_frame)
    vehicle_update_type_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(vehicle_update_frame, text="Capacity").grid(row=2, column=0, sticky="w")
    vehicle_update_capacity_entry = tk.Entry(vehicle_update_frame)
    vehicle_update_capacity_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(vehicle_update_frame, text="Maintenance Due Date").grid(row=3, column=0, sticky="w")
    vehicle_update_maintenance_entry = tk.Entry(vehicle_update_frame)
    vehicle_update_maintenance_entry.grid(row=3, column=1, padx=5, pady=2)

    tk.Label(vehicle_update_frame, text="Availability Status").grid(row=4, column=0, sticky="w")
    vehicle_update_status_entry = ttk.Combobox(vehicle_update_frame, values=VEHICLE_STATUS_OPTIONS, state="readonly")
    vehicle_update_status_entry.grid(row=4, column=1, padx=5, pady=2)
    vehicle_update_status_entry.set(VEHICLE_STATUS_OPTIONS[0])

    tk.Label(vehicle_update_frame, text="Assigned Warehouse ID").grid(row=5, column=0, sticky="w")
    vehicle_update_warehouse_entry = tk.Entry(vehicle_update_frame)
    vehicle_update_warehouse_entry.grid(row=5, column=1, padx=5, pady=2)

    tk.Button(vehicle_update_frame, text="Update Vehicle", command=update_vehicle_gui).grid(
        row=6, column=0, columnspan=2, pady=5
    )

    driver_frame = tk.LabelFrame(top_container, text="Add Driver", padx=10, pady=10)
    driver_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(driver_frame, text="Full Name").grid(row=0, column=0, sticky="w")
    driver_name_entry = tk.Entry(driver_frame)
    driver_name_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(driver_frame, text="Phone").grid(row=1, column=0, sticky="w")
    driver_phone_entry = tk.Entry(driver_frame)
    driver_phone_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(driver_frame, text="Licence Number").grid(row=2, column=0, sticky="w")
    driver_license_entry = tk.Entry(driver_frame)
    driver_license_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(driver_frame, text="Licence Expiry").grid(row=3, column=0, sticky="w")
    driver_expiry_entry = tk.Entry(driver_frame)
    driver_expiry_entry.grid(row=3, column=1, padx=5, pady=2)

    tk.Label(driver_frame, text="Route History Notes").grid(row=4, column=0, sticky="w")
    driver_notes_entry = tk.Entry(driver_frame, width=40)
    driver_notes_entry.grid(row=4, column=1, padx=5, pady=2)

    tk.Label(driver_frame, text="Shift Assignment").grid(row=5, column=0, sticky="w")
    driver_shift_entry = tk.Entry(driver_frame)
    driver_shift_entry.grid(row=5, column=1, padx=5, pady=2)

    tk.Button(driver_frame, text="Add Driver", command=submit_driver).grid(
        row=6, column=0, columnspan=2, pady=5
    )

    inventory_frame = tk.LabelFrame(top_container, text="Add Inventory Item", padx=10, pady=10)
    inventory_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(inventory_frame, text="Item Name").grid(row=0, column=0, sticky="w")
    inventory_name_entry = tk.Entry(inventory_frame)
    inventory_name_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(inventory_frame, text="Description").grid(row=1, column=0, sticky="w")
    inventory_desc_entry = tk.Entry(inventory_frame, width=40)
    inventory_desc_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(inventory_frame, text="Category").grid(row=2, column=0, sticky="w")
    inventory_category_entry = tk.Entry(inventory_frame)
    inventory_category_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(inventory_frame, text="Unit Price").grid(row=3, column=0, sticky="w")
    inventory_price_entry = tk.Entry(inventory_frame)
    inventory_price_entry.grid(row=3, column=1, padx=5, pady=2)

    tk.Button(inventory_frame, text="Add Inventory Item", command=submit_inventory_item).grid(
        row=4, column=0, columnspan=2, pady=5
    )

    warehouse_inventory_frame = tk.LabelFrame(top_container, text="Add Warehouse Inventory", padx=10, pady=10)
    warehouse_inventory_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(warehouse_inventory_frame, text="Warehouse ID").grid(row=0, column=0, sticky="w")
    warehouse_inventory_warehouse_entry = tk.Entry(warehouse_inventory_frame)
    warehouse_inventory_warehouse_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(warehouse_inventory_frame, text="Item ID").grid(row=1, column=0, sticky="w")
    warehouse_inventory_item_entry = tk.Entry(warehouse_inventory_frame)
    warehouse_inventory_item_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(warehouse_inventory_frame, text="Quantity").grid(row=2, column=0, sticky="w")
    warehouse_inventory_quantity_entry = tk.Entry(warehouse_inventory_frame)
    warehouse_inventory_quantity_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(warehouse_inventory_frame, text="Reorder Level").grid(row=3, column=0, sticky="w")
    warehouse_inventory_reorder_entry = tk.Entry(warehouse_inventory_frame)
    warehouse_inventory_reorder_entry.grid(row=3, column=1, padx=5, pady=2)

    tk.Label(warehouse_inventory_frame, text="Item Location").grid(row=4, column=0, sticky="w")
    warehouse_inventory_location_entry = tk.Entry(warehouse_inventory_frame)
    warehouse_inventory_location_entry.grid(row=4, column=1, padx=5, pady=2)


    tk.Button(warehouse_inventory_frame, text="Add Warehouse Inventory", command=submit_warehouse_inventory).grid(
        row=5, column=0, columnspan=2, pady=5
    )

    tk.Label(warehouse_inventory_frame, text="Quantity Change (+/-)").grid(row=6, column=0, sticky="w")
    warehouse_inventory_update_entry = tk.Entry(warehouse_inventory_frame)
    warehouse_inventory_update_entry.grid(row=6, column=1, padx=5, pady=2)

    tk.Button(
        warehouse_inventory_frame,
        text="Update Inventory",
        command=update_inventory_gui
    ).grid(row=7, column=0, columnspan=2, pady=5)

    assignment_frame = tk.LabelFrame(top_container, text="Assign Delivery", padx=10, pady=10)
    assignment_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(assignment_frame, text="Shipment ID").grid(row=0, column=0, sticky="w")
    assignment_shipment_entry = tk.Entry(assignment_frame)
    assignment_shipment_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(assignment_frame, text="Driver ID").grid(row=1, column=0, sticky="w")
    assignment_driver_entry = tk.Entry(assignment_frame)
    assignment_driver_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(assignment_frame, text="Vehicle ID").grid(row=2, column=0, sticky="w")
    assignment_vehicle_entry = tk.Entry(assignment_frame)
    assignment_vehicle_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(assignment_frame, text="Route Details").grid(row=3, column=0, sticky="w")
    assignment_route_entry = tk.Entry(assignment_frame, width=40)
    assignment_route_entry.grid(row=3, column=1, padx=5, pady=2)

    tk.Label(assignment_frame, text="Delivery Date").grid(row=4, column=0, sticky="w")
    assignment_date_entry = tk.Entry(assignment_frame)
    assignment_date_entry.grid(row=4, column=1, padx=5, pady=2)

    tk.Label(assignment_frame, text="Dispatch Time").grid(row=5, column=0, sticky="w")
    assignment_dispatch_entry = tk.Entry(assignment_frame)
    assignment_dispatch_entry.grid(row=5, column=1, padx=5, pady=2)

    tk.Label(assignment_frame, text="Arrival Time").grid(row=6, column=0, sticky="w")
    assignment_arrival_entry = tk.Entry(assignment_frame)
    assignment_arrival_entry.grid(row=6, column=1, padx=5, pady=2)

    tk.Label(assignment_frame, text="Assignment Status").grid(row=7, column=0, sticky="w")
    assignment_status_entry = ttk.Combobox(assignment_frame, values=ASSIGNMENT_STATUS_OPTIONS, state="readonly")
    assignment_status_entry.grid(row=7, column=1, padx=5, pady=2)
    assignment_status_entry.set(ASSIGNMENT_STATUS_OPTIONS[0])

    tk.Button(assignment_frame, text="Assign Delivery", command=submit_delivery_assignment).grid(
        row=8, column=0, columnspan=2, pady=5
    )

    delivery_update_frame = tk.LabelFrame(top_container, text="Update Delivery Assignment", padx=10, pady=10)
    delivery_update_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(delivery_update_frame, text="Assignment ID").grid(row=0, column=0, sticky="w")
    delivery_update_id_entry = tk.Entry(delivery_update_frame)
    delivery_update_id_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(delivery_update_frame, text="New Driver ID").grid(row=1, column=0, sticky="w")
    delivery_update_driver_entry = tk.Entry(delivery_update_frame)
    delivery_update_driver_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(delivery_update_frame, text="New Vehicle ID").grid(row=2, column=0, sticky="w")
    delivery_update_vehicle_entry = tk.Entry(delivery_update_frame)
    delivery_update_vehicle_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(delivery_update_frame, text="New Route Details").grid(row=3, column=0, sticky="w")
    delivery_update_route_entry = tk.Entry(delivery_update_frame, width=40)
    delivery_update_route_entry.grid(row=3, column=1, padx=5, pady=2)

    tk.Label(delivery_update_frame, text="New Delivery Date").grid(row=4, column=0, sticky="w")
    delivery_update_date_entry = tk.Entry(delivery_update_frame)
    delivery_update_date_entry.grid(row=4, column=1, padx=5, pady=2)

    tk.Label(delivery_update_frame, text="New Dispatch Time").grid(row=5, column=0, sticky="w")
    delivery_update_dispatch_entry = tk.Entry(delivery_update_frame)
    delivery_update_dispatch_entry.grid(row=5, column=1, padx=5, pady=2)

    tk.Label(delivery_update_frame, text="New Arrival Time").grid(row=6, column=0, sticky="w")
    delivery_update_arrival_entry = tk.Entry(delivery_update_frame)
    delivery_update_arrival_entry.grid(row=6, column=1, padx=5, pady=2)

    tk.Label(delivery_update_frame, text="New Status").grid(row=7, column=0, sticky="w")
    delivery_update_status_entry = ttk.Combobox(delivery_update_frame, values=ASSIGNMENT_STATUS_OPTIONS,state="readonly")
    delivery_update_status_entry.grid(row=7, column=1, padx=5, pady=2)
    delivery_update_status_entry.set(ASSIGNMENT_STATUS_OPTIONS[0])

    tk.Button(
        delivery_update_frame,
        text="Update Delivery Assignment",
        command=update_delivery_assignment_gui
    ).grid(row=8, column=0, columnspan=2, pady=5)

    incident_frame = tk.LabelFrame(top_container, text="Record Incident", padx=10, pady=10)
    incident_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(incident_frame, text="Shipment ID").grid(row=0, column=0, sticky="w")
    incident_shipment_entry = tk.Entry(incident_frame)
    incident_shipment_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(incident_frame, text="Incident Type").grid(row=1, column=0, sticky="w")
    incident_type_entry = tk.Entry(incident_frame)
    incident_type_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(incident_frame, text="Description").grid(row=2, column=0, sticky="w")
    incident_desc_entry = tk.Entry(incident_frame, width=40)
    incident_desc_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(incident_frame, text="Resolution Status").grid(row=3, column=0, sticky="w")
    incident_status_entry = ttk.Combobox(incident_frame, values=INCIDENT_STATUS_OPTIONS, state="readonly")
    incident_status_entry.grid(row=3, column=1, padx=5, pady=2)
    incident_status_entry.set(INCIDENT_STATUS_OPTIONS[0])

    tk.Button(incident_frame, text="Record Incident", command=submit_incident).grid(
        row=4, column=0, columnspan=2, pady=5
    )

    search_frame = tk.LabelFrame(top_container, text="Search / Filter Shipments", padx=10, pady=10)
    search_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(search_frame, text="Search by Order Number").grid(row=0, column=0, sticky="w")
    search_order_entry = tk.Entry(search_frame)
    search_order_entry.grid(row=0, column=1, padx=5, pady=2)
    tk.Button(search_frame, text="Search", command=search_shipments).grid(row=0, column=2, padx=5, pady=2)

    tk.Label(search_frame, text="Filter by Status").grid(row=1, column=0, sticky="w")
    filter_status_entry = ttk.Combobox(search_frame, values=SHIPMENT_STATUS_OPTIONS, state="readonly")
    filter_status_entry.grid(row=1, column=1, padx=5, pady=2)
    filter_status_entry.set(SHIPMENT_STATUS_OPTIONS[0])

    tk.Button(search_frame, text="Filter", command=filter_shipments).grid(row=1, column=2, padx=5, pady=2)

    payment_frame = tk.LabelFrame(top_container, text="Add Payment", padx=10, pady=10)
    payment_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(payment_frame, text="Shipment ID").grid(row=0, column=0, sticky="w")
    payment_shipment_entry = tk.Entry(payment_frame)
    payment_shipment_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(payment_frame, text="Amount Due").grid(row=1, column=0, sticky="w")
    payment_amount_due_entry = tk.Entry(payment_frame)
    payment_amount_due_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(payment_frame, text="Amount Paid").grid(row=2, column=0, sticky="w")
    payment_amount_paid_entry = tk.Entry(payment_frame)
    payment_amount_paid_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(payment_frame, text="Payment Method").grid(row=3, column=0, sticky="w")
    payment_method_entry = tk.Entry(payment_frame)
    payment_method_entry.grid(row=3, column=1, padx=5, pady=2)

    tk.Label(payment_frame, text="Payment Date (YYYY-MM-DD)").grid(row=4, column=0, sticky="w")
    payment_date_entry = tk.Entry(payment_frame)
    payment_date_entry.grid(row=4, column=1, padx=5, pady=2)

    tk.Label(payment_frame, text="Payment Status").grid(row=5, column=0, sticky="w")
    payment_status_new_entry = ttk.Combobox(payment_frame, values=PAYMENT_STATUS_OPTIONS, state="readonly")
    payment_status_new_entry.grid(row=5, column=1, padx=5, pady=2)
    payment_status_new_entry.set(PAYMENT_STATUS_OPTIONS[0])

    tk.Button(payment_frame, text="Add Payment", command=submit_payment).grid(
        row=6, column=0, columnspan=2, pady=5
    )

    payment_status_frame = tk.LabelFrame(top_container, text="Update Payment Status", padx=10, pady=10)
    payment_status_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(payment_status_frame, text="Payment ID").grid(row=0, column=0, sticky="w")
    payment_update_id_entry = tk.Entry(payment_status_frame)
    payment_update_id_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(payment_status_frame, text="New Status").grid(row=1, column=0, sticky="w")
    payment_update_status_entry = ttk.Combobox(payment_status_frame, values=PAYMENT_STATUS_OPTIONS, state="readonly")
    payment_update_status_entry.grid(row=1, column=1, padx=5, pady=2)
    payment_update_status_entry.set(PAYMENT_STATUS_OPTIONS[0])

    tk.Button(payment_status_frame, text="Update Payment Status", command=change_payment_status).grid(
        row=2, column=0, columnspan=2, pady=5
    )

    if has_role(current_user, ["admin"]):
        users_frame = tk.LabelFrame(top_container, text="Register New User (Admin Only)", padx=10, pady=10)
        users_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(users_frame, text="Username").grid(row=0, column=0, sticky="w")
        reg_username_entry = tk.Entry(users_frame)
        reg_username_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(users_frame, text="Password").grid(row=1, column=0, sticky="w")
        reg_password_entry = tk.Entry(users_frame, show="*")
        reg_password_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(users_frame, text="Role").grid(row=2, column=0, sticky="w")
        reg_role_entry = ttk.Combobox(users_frame, values=ROLE_OPTIONS, state="readonly")
        reg_role_entry.grid(row=2, column=1, padx=5, pady=2)
        reg_role_entry.set(ROLE_OPTIONS[0])

        tk.Label(users_frame, text="Full Name").grid(row=3, column=0, sticky="w")
        reg_full_name_entry = tk.Entry(users_frame)
        reg_full_name_entry.grid(row=3, column=1, padx=5, pady=2)

        tk.Label(users_frame, text="Email").grid(row=4, column=0, sticky="w")
        reg_email_entry = tk.Entry(users_frame)
        reg_email_entry.grid(row=4, column=1, padx=5, pady=2)

        tk.Button(users_frame, text="Register User", command=register_new_user).grid(
            row=5, column=0, columnspan=2, pady=5
        )

    # -------------------------
    # OUTPUT SECTION
    # -------------------------

    output_frame = tk.LabelFrame(bottom_container, text="System Output", padx=10, pady=10)
    output_frame.pack(fill="both", expand=True, padx=10, pady=5)

    button_row_1 = tk.Frame(output_frame)
    button_row_1.pack(fill="x", pady=2)

    tk.Button(button_row_1, text="Show All Customers", command=show_customers).pack(side="left", padx=4)
    tk.Button(button_row_1, text="Show All Warehouses", command=show_warehouses).pack(side="left", padx=4)
    tk.Button(button_row_1, text="Show All Shipments", command=show_shipments).pack(side="left", padx=4)
    tk.Button(button_row_1, text="Show All Vehicles", command=show_vehicles).pack(side="left", padx=4)

    button_row_2 = tk.Frame(output_frame)
    button_row_2.pack(fill="x", pady=2)

    tk.Button(button_row_2, text="Show All Drivers", command=show_drivers).pack(side="left", padx=4)
    tk.Button(button_row_2, text="Show Inventory by Warehouse", command=show_inventory).pack(side="left", padx=4)
    tk.Button(button_row_2, text="Show Delivery Assignments", command=show_delivery_assignments).pack(side="left", padx=4)
    tk.Button(button_row_2, text="Show Incidents", command=show_incidents).pack(side="left", padx=4)

    button_row_3 = tk.Frame(output_frame)
    button_row_3.pack(fill="x", pady=2)

    tk.Button(button_row_3, text="Show All Payments", command=show_payments).pack(side="left", padx=4)
    tk.Button(button_row_3, text="Shipment Status Report", command=show_shipment_status_report).pack(side="left", padx=4)
    tk.Button(button_row_3, text="Vehicle Utilisation Report", command=show_vehicle_utilisation_report).pack(side="left", padx=4)
    tk.Button(button_row_3, text="Warehouse Activity Report", command=show_warehouse_activity_report).pack(side="left", padx=4)

    if has_role(current_user, ["admin"]):
        button_row_4 = tk.Frame(output_frame)
        button_row_4.pack(fill="x", pady=2)
        tk.Button(button_row_4, text="Show All Users", command=show_users).pack(side="left", padx=4)

    output_box = tk.Text(output_frame, height=18, width=130, wrap="word")
    output_box.pack(fill="both", expand=True, padx=5, pady=10)

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



login_root: Tk = tk.Tk()
login_root.title("Login - Northshore Logistics System")
login_root.geometry("400x250")

tk.Label(login_root, text="Northshore Logistics Login", font=("Arial", 14, "bold")).pack(pady=15)

login_frame = tk.Frame(login_root)
login_frame.pack(pady=10)

tk.Label(login_frame, text="Username").grid(row=0, column=0, padx=5, pady=5)
login_username_entry: Entry = tk.Entry(login_frame)
login_username_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(login_frame, text="Password").grid(row=1, column=0, padx=5, pady=5)
login_password_entry: Entry = tk.Entry(login_frame, show="*")
login_password_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(login_root, text="Login", command=attempt_login).pack(pady=15)

login_root.mainloop()