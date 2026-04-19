import tkinter as tk
from tkinter import messagebox
from services.shipment_service import add_shipment

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

root = tk.Tk()
root.title("Northshore Logistics System")
root.geometry("500x500")

tk.Label(root, text="Order Number").pack()
order_entry = tk.Entry(root)
order_entry.pack()

tk.Label(root, text="Sender Customer ID").pack()
sender_entry = tk.Entry(root)
sender_entry.pack()

tk.Label(root, text="Receiver Customer ID").pack()
receiver_entry = tk.Entry(root)
receiver_entry.pack()

tk.Label(root, text="Item Description").pack()
item_entry = tk.Entry(root)
item_entry.pack()

tk.Label(root, text="Origin Warehouse ID").pack()
warehouse_entry = tk.Entry(root)
warehouse_entry.pack()

tk.Label(root, text="Destination Address").pack()
address_entry = tk.Entry(root)
address_entry.pack()

tk.Label(root, text="Transport Cost").pack()
cost_entry = tk.Entry(root)
cost_entry.pack()

tk.Label(root, text="Surcharge").pack()
surcharge_entry = tk.Entry(root)
surcharge_entry.pack()

tk.Label(root, text="Payment Status").pack()
payment_entry = tk.Entry(root)
payment_entry.pack()

tk.Button(root, text="Add Shipment", command=submit_shipment).pack(pady=10)

root.mainloop()