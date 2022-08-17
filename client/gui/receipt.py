import tkinter as tk
from tkinter import ttk
from client.gui.item import GuiItem
from receipt import Receipt

class GuiReceipt(ttk.Frame):
    def __init__(self, container, sharer_names, starting_items=5):


        super().__init__(container)
        self.container = container
        self.items = []
        self.sharer_names = sharer_names
        self.create_widgets()
        self.format_widgets()

        self.underlying_receipt = None
        self.dirty = True

        for ii in range(starting_items):
            self.create_item()


    def make_dirty(self):
        self.dirty = True

    def update_underlying_receipt(self):
        if not(self.dirty):
            return
        if self.underlying_receipt == None:
            self.underlying_receipt = Receipt(
                    self.payer_entry.get(),
                    self.date_entry.get(),
                    from_client=True,
                    client=self.container.get_client()
                    )
            for item in self.items:
                item.update_underlying_item()
                self.underlying_receipt.add_item(item.underlying_item)
        else:
            self.underlying_receipt.clear_items()
            for item in self.items:
                item.update_underlying_item()
                self.underlying_receipt.add_item(item.underlying_item)
                self.underlying_receipt.payer = self.payer_entry.get()
                self.underlying_receipt.date = self.date_entry.get()
        self.dirty = False


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
        self.grid()

    def create_widgets(self):

        self.payer_label = ttk.Label(self, text="Paid by")

        self.date_label = ttk.Label(self, text="Date")

        self.payer_entry = ttk.Entry(self, width=10)
        self.date_entry = ttk.Entry(self, width=10)


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

    def update_cost_labels(self):
        self.make_dirty()
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
            print("WARNING: Unable to find item to remove from receipt")
            return

        for item in self.items[item_idx+1:]:
            item.shift_up_row()
        
        self.items.pop(item_idx)


    def create_item(self):
        self.items.append(GuiItem(self, len(self.items)+1))
        self.format_widgets()
