import tkinter as tk
from client.gui.connect_screen import ConnectScreen

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Money Splitter v0.1")

        connect_screen = ConnectScreen(self)
