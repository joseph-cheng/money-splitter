import tkinter as tk
from tkinter import ttk
from client.gui.receipt import GuiReceipt

class GuiReceiptEditor(ttk.Frame):
    def __init__(self, container, database):
        super().__init__(container)
        self.container = container
        self.database = database



        self.gui_receipts = {}
        if self.database != None:
            for receipt in self.database.get_all_receipts():
                r = GuiReceipt.create_from_data(receipt, self)
                self.gui_receipts[receipt.id] = r
                r.grid_forget()

        if len(self.gui_receipts) != 0:
            self.chosen_receipt_id = list(self.gui_receipts.keys())[0]
        else:
            self.chosen_receipt_id = None

        receipt_selector_var = tk.StringVar()
        receipt_names = [self.receipt_id_to_option(receipt_id) for receipt_id in self.gui_receipts.keys()]
        self.receipt_selector = ttk.OptionMenu(self,
                receipt_selector_var,
                default=self.receipt_id_to_option(self.chosen_receipt_id),
                *receipt_names,
                )

    def receipt_id_to_option(self, receipt_id):
        if receipt_id == None:
            return ""
        return f"{self.gui_receipts[receipt_id].get_underlying_receipt().date} - receipt_id"

    def choose_receipt(self, receipt_id):
        if self.chosen_receipt_id != None:
            self.gui_receipts[self.chosen_receipt_id].grid_forget()
        self.gui_receipts[receipt_id].grid()



