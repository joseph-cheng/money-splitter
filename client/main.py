from client.client import Client
from PyQt5.QtWidgets import QApplication, QLabel
from client.gui.app import App


def run_client(client):
    client.init("localhost", 1337)


if __name__ == "__main__":

    """
    app = QApplication([])
    label = QLabel("Hello, world!")
    label.show()
    app.exec()
    """

    client = Client()
    app = App(client)
    app.after(0, lambda client=client: run_client(client))
    app.mainloop()
    client.deinit()
