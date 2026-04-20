import tkinter as tk
from tkinter import messagebox
from services.shipment_service import add_shipment, get_all_shipments, update_shipment_status
from services.customer_service import add_customer, get_all_customers
from services.warehouse_service import add_warehouse, get_all_warehouses


def submit_customer():
    try:
        add_customer(
            customer_name_entry.get(),
            customer_phone_entry.get(),
            customer_email_entry.get(),
            customer_address_entry.get()
        )
        messagebox.showinfo("Success", "Customer added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def submit_warehouse():
    try:
        add_warehouse(
            warehouse_name_entry.get(),
            warehouse_city_entry.get(),
            warehouse_address_entry.get(),
            warehouse_manager_entry.get()
        )
        messagebox.showinfo("Success", "Warehouse added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def submit_shipment():
    try:
        add_shipment(
            order_entry.get(),
            int(sender_entry.get()),
            int(receiver_entry.get()),
            item_entry.get(),
            int(warehouse_entry.get()),
            address_entry.get(),
            float(cost_entry.get()),
            float(surcharge_entry.get()),
            payment_entry.get()
        )
        messagebox.showinfo("Success", "Shipment added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_shipments():
    records = get_all_shipments()
    output_box.delete("1.0", tk.END)

    for row in records:
        output_box.insert(
            tk.END,
            f"Shipment ID: {row[0]} | Order: {row[1]} | Status: {row[7]} | Cost: {row[8]}\n"
        )


def change_status():
    try:
        update_shipment_status(
            int(status_shipment_id_entry.get()),
            status_entry.get()
        )
        messagebox.showinfo("Success", "Shipment status updated.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_customers():
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


def show_warehouses():
    try:
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

root = tk.Tk()
root.title("Northshore Logistics System")
root.geometry("900x750")

title = tk.Label(root, text="Northshore Logistics Database System", font=("Arial", 16, "bold"))
title.pack(pady=10)

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

output_frame = tk.LabelFrame(root, text="System Output", padx=10, pady=10)
output_frame.pack(fill="both", expand=True, padx=10, pady=5)

tk.Button(output_frame, text="Show All Customers", command=show_customers).pack(pady=5)
tk.Button(output_frame, text="Show All Warehouses", command=show_warehouses).pack(pady=5)
tk.Button(output_frame, text="Show All Shipments", command=show_shipments).pack(pady=5)

output_box = tk.Text(output_frame, height=15, width=100)
output_box.pack()

root.mainloop()