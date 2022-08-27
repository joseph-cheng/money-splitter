import logging
import tkinter as tk
import config
from tkinter import ttk
from client.client import Client
from client.gui.password_screen import PasswordScreen

class ConnectScreen(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container

        self.create_widgets()
        self.format_widgets()

    def format_widgets(self):
        self.ip_entry.grid(column=0, row=0)
        self.port_entry.grid(column=0, row=1)
        self.connect_button.grid(column=0, row=2)
        self.grid()

    def create_widgets(self):
        self.ip_var = tk.StringVar()
        self.ip_entry = ttk.Entry(self, width=20, textvariable=self.ip_var)

        self.port_var = tk.StringVar()
        self.port_entry = ttk.Entry(self, width=5, textvariable=self.port_var)

        self.ip_var.set(config.default_host)
        self.port_var.set(str(config.default_port))

        self.connect_button = ttk.Button(self, text="Connect", command=self.connect)

        self.ip_entry.bind("<Return>", lambda _: self.connect())
        self.port_entry.bind("<Return>", lambda _: self.connect())
        self.ip_entry.focus_set()

    def connect(self):
        ip = self.ip_var.get()
        try:
            port = int(self.port_var.get())
        except:
            logging.error("Port is not a number, not connecting")
            return

        client = Client()
        client.init(ip, port)

        password_screen = PasswordScreen(self.container, client)

        self.grid_forget()




