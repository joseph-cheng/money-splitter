import logging
import tkinter as tk
import config
from tkinter import ttk
from client.gui.item import GuiItem
from receipt import Receipt

class GuiReceipt(ttk.Frame):
    def __init__(self, container, sharer_names, starting_items=5, underlying_receipt=None):


        super().__init__(container)
        self.container = container
        self.items = []
        self.sharer_names = sharer_names
        self.underlying_receipt = underlying_receipt
        self.create_widgets()
        self.format_widgets()

        
        if self.underlying_receipt is None:
            self.make_dirty()
            self.trace_variables()
        else:
            self.dirty = False

        for ii in range(starting_items):
            self.create_item()


    def make_dirty(self):

        self.dirty = True
        if self.underlying_receipt is not None:
            self.container.acknowledge_changed_receipt(self.underlying_receipt.id)

    def update_underlying_receipt(self):
        if not(self.dirty):
            return
        if self.underlying_receipt == None:
            self.underlying_receipt = Receipt(
                    self.payer_var.get(),
                    self.date_var.get(),
                    from_client=True,
                    client=self.container.get_client()
                    )
            for item in self.items:
                underlying_item = item.get_underlying_item()
                self.underlying_receipt.add_item(underlying_item)
        else:
            self.underlying_receipt.clear_items()
            for item in self.items:
                underlying_item = item.get_underlying_item()
                self.underlying_receipt.add_item(underlying_item)
                self.underlying_receipt.payer = self.payer_var.get()
                self.underlying_receipt.date = self.date_var.get()
        self.dirty = False

    def get_underlying_receipt(self):
        if self.dirty:
            self.update_underlying_receipt()
        if self.underlying_receipt is None:
            logging.warning("Returning non-existent underlying receipt as None")
        return self.underlying_receipt


    def format_widgets(self):
        options= {'padx':5, 'pady': 5}
        self.payer_label.grid(column=0, row=0, sticky=tk.W, **options)
        self.date_label.grid(column=1, row=0, sticky=tk.W, **options)
        self.payer_entry.grid(column=0, row=1, sticky=tk.W, **options)
        self.date_entry.grid(column=1, row=1, sticky=tk.W, **options)
        self.name_label.grid(column=2, row=0, sticky=tk.W, **options)
        self.quantity_label.grid(column=3, row=0, sticky=tk.W, **options)
        self.price_label.grid(column=4, row=0, sticky=tk.W, **options)
        self.incomplete_label.grid(column=5, row=0, sticky=tk.W, **options)

        for ii, sharer in enumerate(self.sharer_names):
            self.sharer_labels[ii].grid(column=6+ii, row=0)

        self.granular_label.grid(column=12, row=0, **options)
        self.add_item_button.grid(column=2, row=len(self.items)+2)
        self.cost_label.grid(column=4, row=len(self.items)+2, sticky=tk.W, **options)
        for ii, sharer_cost_label in enumerate(self.sharer_cost_labels):
            sharer_cost_label.grid(column=6+ii, row=len(self.items)+2, sticky=tk.W, **options)
        self.delete_receipt_button.grid(column=0, row=len(self.items)+3)
        self.grid()

    def create_widgets(self):

        self.delete_receipt_button = ttk.Button(self, text="Delete Receipt", command=self.delete)
        self.payer_label = ttk.Label(self, text="Paid by")

        self.date_label = ttk.Label(self, text="Date")

        
        self.payer_var = tk.StringVar()
        self.payer_entry = ttk.Entry(self, width=10, textvariable=self.payer_var)

        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(self, width=10, textvariable=self.date_var)



        self.name_label = ttk.Label(self, text="Item")

        self.quantity_label = ttk.Label(self, text="Quantity")

        self.price_label = ttk.Label(self, text="Price")

        self.incomplete_label = ttk.Label(self, text="Incomplete?")

        self.sharer_labels = []

        for ii, sharer in enumerate(self.sharer_names):
            self.sharer_labels.append(ttk.Label(self, text=sharer))


        self.granular_label = ttk.Label(self, text="Precise?")

        self.add_item_button = ttk.Button(self, text="Add Item", command=self.create_item)

        self.cost_label = ttk.Label(self, text="0.00")

        self.sharer_cost_labels = []
        for sharer in self.sharer_names:
            self.sharer_cost_labels.append(ttk.Label(self, text="0.00"))


        self.payer_entry.focus_set()

    def delete(self):
        rid = self.get_underlying_receipt().id
        self.container.remove_receipt(rid)
        self.grid_forget()

    def update_cost_labels(self):
        sharer_total_contributions = [0 for _ in self.sharer_names]
        for item in self.items:
            sharer_contributions = item.get_sharer_contributions()
            for ii, sharer_contribution in enumerate(sharer_contributions):
                sharer_total_contributions[ii] += sharer_contributions[ii]

        self.cost_label.config(text=str(round(sum(sharer_total_contributions), 2)))
        for ii, sharer_cost_label in enumerate(self.sharer_cost_labels):
            sharer_cost_label.config(text=str(round(sharer_total_contributions[ii], 2)))



    def remove_item(self, item_to_remove):
        item_idx = -1
        for ii, item in enumerate(self.items):
            if item == item_to_remove:
                item_idx = ii
                break

        if item_idx == -1:
            logging.warning("Unable to find item to remove from receipt")
            return

        for item in self.items[item_idx+1:]:
            item.shift_up_row()
        
        self.items.pop(item_idx)


    def create_item(self):
        self.items.append(GuiItem(self, len(self.items)+1))
        self.format_widgets()
        self.add_item_button.tkraise()

    def trace_variables(self):
        self.payer_var.trace("w", lambda *_: self.make_dirty())
        self.date_var.trace("w", lambda *_: self.make_dirty())

    @staticmethod
    def create_from_data(receipt, container):
        if len(receipt.items) == 0:
            sharer_names = config.default_sharer_names
        else:
            sharer_names = list(receipt.items[0].sharers.keys())
        ret = GuiReceipt(container, sharer_names, starting_items=0, underlying_receipt=receipt)
        for ii, item in enumerate(receipt.items):
            ret.items.append(GuiItem.create_from_data(item, ret, ii+1))

        ret.date_var.set(str(receipt.date))
        ret.payer_var.set(receipt.payer)
        ret.trace_variables()
        ret.format_widgets()
        ret.update_cost_labels()
        ret.add_item_button.tkraise()
        return ret
