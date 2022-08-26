from server.client_handler import ClientHandler
import socket

class Server:


    def __init__(self, dbm):
        self.serversock = None
        self.dbm = dbm

    def init(self, ip, port):
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversock.bind((ip, port))

    def listen(self):
        print("INFO: listening for connections...")
        self.serversock.listen(5)

        while True:
            conn, addr = self.serversock.accept()
            print(f"INFO: connection accepted from {addr}")
            ch = ClientHandler(conn, self.dbm)
            ch.start()



