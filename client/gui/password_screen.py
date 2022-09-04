import tkinter as tk
import config
from tkinter import ttk
from client.gui.main_screen import MainScreen

class PasswordScreen(ttk.Frame):
    def __init__(self, container, client):
        super().__init__(container)
        self.container = container
        self.client = client

        self.create_widgets()
        self.format_widgets()


    def create_widgets(self):
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self, width=20, textvariable=self.password_var)

        self.enter_button = ttk.Button(self, text="Enter Password", command=self.send_password)

        self.password_entry.bind("<Return>", lambda _: self.send_password())
        self.password_entry.focus_set()

    def format_widgets(self):
        self.password_entry.grid(column=0, row=0)
        self.enter_button.grid(column=0, row=1)
        self.grid()

    def send_password(self):
        password = self.password_var.get()
        self.client.send_message(password.encode("utf-8"))
        okay = int.from_bytes(self.client.receive_message(msg_len=1), byteorder=config.endianness)
        if okay:
            self.client.download_db()
            main_screen = MainScreen(self.container, self.client)
            self.grid_forget()



