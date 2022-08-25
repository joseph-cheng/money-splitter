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
    client.init("localhost", 1337)
    app = App(client)
    app.mainloop()
    client.deinit()
