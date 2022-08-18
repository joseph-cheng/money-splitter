import tkinter as tk
from client.gui.receipt import GuiReceipt
from client.gui.receipt_editor import GuiReceiptEditor

class App(tk.Tk):
    def __init__(self, client):
        super().__init__()
        self.client = client

        self.title("Money Splitter v0.1")


        receipt_editor = GuiReceiptEditor(self, self.client.database)
        #receipt = GuiReceipt(self, ["Zixiao", "Joe", "Robbie"])

    def get_client(self):
        return self.client
