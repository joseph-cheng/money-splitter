from client.client import Client
from client.gui.app import App
from tkinter import ttk




if __name__ == "__main__":



    app = App()
    app.style = ttk.Style()
    app.style.theme_use("clam")
    app.mainloop()
