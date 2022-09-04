import tkinter as tk
from tkinter import ttk
from client.gui.receipt_editor import GuiReceiptEditor
from client.gui.debt import DebtScreen

class MainScreen(ttk.Frame):
    def __init__(self, container, client):
        super().__init__(container)
        self.container = container
        self.client = client

        self.create_widgets()
        self.format_widgets()

    def create_widgets(self):
        self.receipt_editor = GuiReceiptEditor(self, self.client)
        self.debt_screen = DebtScreen(self, self.client)

    def format_widgets(self):
        self.receipt_editor.grid(column=0, row=0)
        self.debt_screen.grid(column=1, row=0)
        self.grid()

    def update_debts(self):
        self.debt_screen.update_debts()


