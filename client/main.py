from client.client import Client
from client.gui.app import App



if __name__ == "__main__":
    app = App()
    app.mainloop()
    client = Client()
    client.init("localhost", 1337)
    client.deinit()


