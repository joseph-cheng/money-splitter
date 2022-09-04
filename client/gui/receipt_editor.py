import tkinter as tk
from tkinter import ttk
from client.gui.receipt import GuiReceipt
from receipt import Receipt
import config

class GuiReceiptEditor(ttk.Frame):
    def __init__(self, container, client):
        super().__init__(container)
        self.container = container
        self.client = client

        self.new_receipt_ids = set()
        self.changed_receipt_ids = set()
        self.removed_receipt_ids = set()

        self.create_widgets()
        self.format_widgets()

    def acknowledge_changed_receipt(self, receipt_id):
        if receipt_id not in self.new_receipt_ids:
            self.changed_receipt_ids.add(receipt_id)

    def remove_receipt(self, rid):
        self.removed_receipt_ids.add(rid)
        self.gui_receipts.pop(rid, None)
        self.chosen_receipt_id = list(self.gui_receipts.keys())[0]
        self.choose_receipt(self.chosen_receipt_id)
        self.update_option_menu()


    def get_client(self):
        return self.client

    def format_widgets(self):
        self.receipt_selector.grid(column=0, row=0)
        self.create_receipt_button.grid(column=0, row=1)
        self.save_changes_button.grid(column=1, row=3)
        if self.chosen_receipt_id is not None:
            chosen_receipt = self.gui_receipts[self.chosen_receipt_id]
            chosen_receipt.grid(column=0, row=2)
        self.grid()

    def create_widgets(self):
        self.gui_receipts = {}
        if self.client.dbm != None:
            for receipt in self.client.dbm.get_all_receipts():
                r = GuiReceipt.create_from_data(receipt, self)
                self.gui_receipts[receipt.id] = r
                r.grid_forget()

        if len(self.gui_receipts) != 0:
            self.chosen_receipt_id = list(self.gui_receipts.keys())[0]
        else:
            self.chosen_receipt_id = None

        self.receipt_selector_var = tk.StringVar()
        self.create_receipt_names()
        self.receipt_selector = ttk.OptionMenu(self,
                self.receipt_selector_var,
                self.receipt_id_to_option(self.chosen_receipt_id),
                *self.receipt_names,
                command=lambda _: self.choose_receipt(),
                )

        self.create_receipt_button = ttk.Button(self, text = "New Receipt", command=self.create_empty_receipt)
        self.save_changes_button = ttk.Button(self, text="Save Changes", command=self.upload_changes)

    def create_receipt_names(self):
        self.receipt_names = [self.receipt_id_to_option(receipt_id) for receipt_id in self.gui_receipts.keys()]


    def receipt_id_to_option(self, receipt_id):
        if receipt_id == None:
            return ""
        separator = ' | '
        return f"{receipt_id}{separator}{self.gui_receipts[receipt_id].get_underlying_receipt().date}"
    
    def option_to_receipt_id(self, option_name):
        # ' | ' is the separator we use for generating the option
        split_option_name = option_name.split(' | ')
        id = Receipt.str_to_id(split_option_name[0])
        return id

    def create_empty_receipt(self):
        # create new gui receipt and underlying receipt object
        new_receipt = GuiReceipt(self, config.default_sharer_names)
        new_receipt.update_underlying_receipt()
        # add it to stored dict of receipts
        self.gui_receipts[new_receipt.underlying_receipt.id] = new_receipt
        # make the new receipt the chosen one
        self.choose_receipt(new_receipt.underlying_receipt.id)

        self.update_option_menu()
        self.new_receipt_ids.add(new_receipt.underlying_receipt.id)

    def update_database(self):
        for receipt_id in self.new_receipt_ids:
            gui_receipt = self.gui_receipts[receipt_id]
            receipt = gui_receipt.get_underlying_receipt()
            self.client.dbm.add_receipt(receipt)

        for receipt_id in self.changed_receipt_ids:
            gui_receipt = self.gui_receipts[receipt_id]
            receipt = gui_receipt.get_underlying_receipt()
            self.client.dbm.update_receipt(receipt)

        for receipt_id in self.removed_receipt_ids:
            self.client.dbm.remove_receipt(receipt_id)

        self.new_receipt_ids = set()
        self.changed_receipt_ids = set()
        self.removed_receipt_ids = set()


    def update_option_menu(self):
        self.create_receipt_names()
        self.receipt_selector.set_menu(self.receipt_id_to_option(self.chosen_receipt_id), *self.receipt_names)


    def save_receipts(self):
        for receipt_id in self.gui_receipts:
            self.gui_receipts[receipt_id].update_underlying_receipt()
        self.update_option_menu()

    def upload_changes(self):
        self.save_receipts()
        self.update_database()
        self.container.update_debts()
        self.client.upload_changes()


    def choose_receipt(self, receipt_id=None):
        # if no receipt id is given, take it from the option menu
        if receipt_id == None:
            receipt_id = self.option_to_receipt_id(self.receipt_selector_var.get())
        if self.chosen_receipt_id != None:
            self.gui_receipts[self.chosen_receipt_id].grid_forget()
        self.gui_receipts[receipt_id].grid()
        self.chosen_receipt_id = receipt_id
        self.save_receipts()



