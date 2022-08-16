import tkinter as tk
from tkinter import ttk
from client.gui.sharers import GuiSharers

class GuiItem:

    def __init__(self, parent_receipt, row):

        self.parent_receipt = parent_receipt
        self.row = row
        self.create_widgets()
        self.format_widgets()

    def format_widgets(self):
        options = {'padx': 5, 'pady': 5}
        self.name_entry.grid(column=0, row=self.row, sticky=tk.W, **options)
        self.price_entry.grid(column=1, row=self.row, sticky=tk.W, **options)
        self.quantity_entry.grid(column=2, row=self.row, sticky=tk.W, **options)
        self.incomplete_button.grid(column=3, row=self.row, **options)
        self.granular_button.grid(column=10, row=self.row, **options)
        self.delete_button.grid(column=11, row=self.row, **options)

    def shift_up_row(self):
        self.row = self.row - 1
        self.sharers.shift_up_row()
        self.format_widgets()


    def create_widgets(self):
        self.name_entry = ttk.Entry(self.parent_receipt, width=15)

        self.price_var = tk.StringVar()
        self.price_var.trace("w", lambda *_: self.parent_receipt.update_cost_labels())
        self.price_entry = ttk.Entry(self.parent_receipt, width=5, textvariable=self.price_var)

        self.quantity_var = tk.StringVar()
        self.quantity_var.trace("w", lambda *_: self.parent_receipt.update_cost_labels())
        self.quantity_entry= ttk.Entry(self.parent_receipt, width=5, textvariable=self.quantity_var)

        self.incomplete = tk.StringVar()
        self.incomplete_button = ttk.Checkbutton(self.parent_receipt, variable=self.incomplete, command=self.parent_receipt.update_cost_labels)

        self.sharers = GuiSharers(self.parent_receipt, 3, self.row)

        self.granular = tk.StringVar()
        self.granular_button = ttk.Checkbutton(self.parent_receipt, variable=self.granular, command=self.sharers.swap)

        self.delete_button = ttk.Button(self.parent_receipt, text="X", command=self.delete)

    def delete(self):
        self.parent_receipt.remove_item(self)
        self.name_entry.grid_forget()
        self.price_entry.grid_forget()
        self.quantity_entry.grid_forget()
        self.incomplete_button.grid_forget()
        self.granular_button.grid_forget()
        self.delete_button.grid_forget()

        self.sharers.delete()

    def get_sharer_contributions(self):
        sharer_portions = self.sharers.get_sharer_values()
        print(sharer_portions)

        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        incomplete = 'selected' in self.incomplete_button.state()

        if incomplete:
            return [0 for _ in sharer_portions]

        total_item_cost = 0
        try:
            total_item_cost = float(price) * float(quantity)
        except:
            print(f"ERROR: unable to calculate total cost of item with price {price} and quantity {quantity}")



        sharer_contributions = [total_item_cost * sharer_portion for sharer_portion in sharer_portions]

        return sharer_contributions
