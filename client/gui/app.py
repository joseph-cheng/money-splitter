import tkinter as tk
from client.gui.receipt import GuiReceipt

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Money Splitter v0.1")


        receipt = GuiReceipt(self, ["Zixiao", "Joe", "Robbie"])

