from client.client import Client
from client.gui.app import App
from tkinter import ttk
import util




if __name__ == "__main__":



    util.setup_logging("client.log")

    app = App()
    app.style = ttk.Style()
    app.style.theme_use("clam")
    app.mainloop()
