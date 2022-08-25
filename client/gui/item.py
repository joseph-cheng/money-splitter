import tkinter as tk
import util
from tkinter import ttk
from client.gui.sharers import GuiSharers
from receipt import ReceiptItem

class GuiItem:

    def __init__(self, parent_receipt, row, underlying_item=None):

        self.parent_receipt = parent_receipt
        self.row = row
        self.underlying_item = underlying_item
        self.create_widgets()
        self.format_widgets()
        if self.underlying_item is None:
            self.trace_variables()
            self.make_dirty()
        else:
            self.dirty = False

    def make_dirty(self):
        self.dirty = True
        self.parent_receipt.make_dirty()

    def get_underlying_item(self):
        if self.dirty:
            self.update_underlying_item()
        return self.underlying_item

    def update_underlying_item(self):
        if not(self.dirty):
            return

        underlying_sharers = self.sharers.get_underlying_sharers()
        if self.underlying_item is None:
            self.underlying_item = ReceiptItem(self.name_var.get(), self.price_var.get(), self.quantity_var.get(), underlying_sharers)
        else:
            print(self.name_var.get())
            self.underlying_item.name = self.name_var.get()
            self.underlying_item.price = self.price_var.get()
            self.underlying_item.quantity = self.quantity_var.get()
            self.underlying_item.sharers = underlying_sharers

        self.dirty = False

    def update_parent_cost_labels(self):
        self.make_dirty()
        self.parent_receipt.update_cost_labels()


    def format_widgets(self):
        options = {'padx': 5, 'pady': 5}
        self.name_entry.grid(column=2, row=self.row, sticky=tk.W, **options)
        self.price_entry.grid(column=3, row=self.row, sticky=tk.W, **options)
        self.quantity_entry.grid(column=4, row=self.row, sticky=tk.W, **options)
        self.incomplete_button.grid(column=5, row=self.row, **options)
        self.delete_button.grid(column=13, row=self.row, **options)

    def shift_up_row(self):
        self.row = self.row - 1
        self.sharers.shift_up_row()
        self.format_widgets()


    def create_widgets(self):
        vcmd = (self.parent_receipt.register(util.is_float))

        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.parent_receipt, textvariable=self.name_var, width=15)

        self.price_var = tk.StringVar()
        self.price_entry = ttk.Entry(self.parent_receipt, width=5, textvariable=self.price_var, validate='all', validatecommand=(vcmd, '%P'))

        self.quantity_var = tk.StringVar()
        self.quantity_entry= ttk.Entry(self.parent_receipt, width=5, textvariable=self.quantity_var, validate='all', validatecommand=(vcmd, '%P'))

        self.incomplete = tk.StringVar()
        self.incomplete_button = ttk.Checkbutton(self.parent_receipt, variable=self.incomplete, command=self.update_parent_cost_labels)


        # if we are creating from data, we will create sharers on our own!
        if self.underlying_item is None:
            self.sharers = GuiSharers(self.parent_receipt, self, 3, self.row, 6, self.parent_receipt.sharer_names)


        self.delete_button = ttk.Button(self.parent_receipt, text="X", command=self.delete)

    def delete(self):
        self.parent_receipt.remove_item(self)
        self.name_entry.grid_forget()
        self.price_entry.grid_forget()
        self.quantity_entry.grid_forget()
        self.incomplete_button.grid_forget()
        self.delete_button.grid_forget()

        self.sharers.delete()

    def trace_variables(self):
        self.name_var.trace("w", lambda *_: self.make_dirty())
        self.price_var.trace("w", lambda *_: self.update_parent_cost_labels())
        self.quantity_var.trace("w", lambda *_: self.update_parent_cost_labels())

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

    @staticmethod
    def create_from_data(item, parent_receipt, row):
        ret = GuiItem(parent_receipt, row, underlying_item=item)
        ret.name_var.set(item.name)
        ret.quantity_var.set(str(item.quantity))
        ret.price_var.set(str(item.price))
        if item.incomplete:
            ret.incomplete_button.state(['selected'])

        ret.sharers = GuiSharers.create_from_data(item.sharers, parent_receipt, ret, row, 6)
        ret.trace_variables()
        return ret
