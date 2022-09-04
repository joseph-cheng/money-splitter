import tkinter as tk
from tkinter import ttk

class DebtScreen(ttk.Frame):
    def __init__(self, container, client):
        super().__init__(container)
        self.container = container
        self.client = client

        self.create_widgets()
        self.format_widgets()

    def calculate_debts(self):
        receipts = self.client.dbm.get_all_receipts()
        debts = {}
        for receipt in receipts:
            receipt_payer = receipt.payer.upper()
            for item in receipt.items:
                for sharer in item.sharers:
                    sharer_contribution = item.get_price_for_sharer(sharer)
                    sharer = sharer.upper()
                    debts[sharer] = debts.get(sharer, 0) - sharer_contribution
                    debts[receipt_payer] = debts.get(receipt_payer, 0) + sharer_contribution

        return debts

                    
    def update_debts(self):
        debts = self.calculate_debts()
        sharer_names = [label["text"] for label in self.sharer_name_labels]
        for sharer in debts:
            try:
                idx = sharer_names.index(sharer)
            except ValueError:
                idx = None
            if idx == None:
                self.sharer_name_labels.append(ttk.Label(self, text=sharer))
                self.sharer_debt_labels.append(tk.Label(self, text=str(round(debts[sharer], 2))))
            else:
                self.sharer_debt_labels[idx]["text"] = str(round(debts[sharer], 2))


            


    def create_widgets(self):
        debts = self.calculate_debts()

        self.sharer_name_labels = []
        self.sharer_debt_labels = []

        for sharer in debts:
            self.sharer_name_labels.append(ttk.Label(self, text=sharer))
            self.sharer_debt_labels.append(ttk.Label(self, text=str(round(debts[sharer], 2))))


    def format_widgets(self):
        for ii, label in enumerate(self.sharer_name_labels):
            label.grid(row=ii, column=0)

        for ii, label in enumerate(self.sharer_debt_labels):
            debt = float(label["text"])
            options = {"width": 5, "anchor": "center"}
            if debt < 0:
                options["background"] = "red"
            else:
                options["background"] = "green"
            label.config(**options)
            label.grid(row=ii, column=1)
        self.grid()



    

