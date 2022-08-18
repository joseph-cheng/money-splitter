import tkinter as tk
from tkinter import ttk

class GuiReceiptEditor(ttk.Frame):
    def __init__(self, container, database):
        super().__init__(container)
        self.container = container
        self.database = database

