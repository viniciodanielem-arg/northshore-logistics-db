import tkinter as tk
from tkinter import messagebox
from typing import Optional
from tkinter import Entry, Text, Tk

from services.auth_service import login_user, register_user, get_all_users
from services.shipment_service import add_shipment, get_all_shipments, update_shipment_status
from services.customer_service import add_customer, get_all_customers
from services.warehouse_service import add_warehouse, get_all_warehouses
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

    if current_user is None:
        raise ValueError("No user is currently logged in.")

    if login_root is not None:
        login_root.destroy()

    root = tk.Tk()
    root.title("Northshore Logistics System")
    root.geometry("1000x850")

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