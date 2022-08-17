from client.client import Client
from PyQt5.QtWidgets import QApplication, QLabel
from client.gui.app import App



if __name__ == "__main__":

    """
    app = QApplication([])
    label = QLabel("Hello, world!")
    label.show()
    app.exec()
    """

    client = Client()
    app = App(client)
    app.mainloop()

    client.init("localhost", 1337)
    client.deinit()


