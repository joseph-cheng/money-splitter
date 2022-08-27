from server.server import Server
from server.dbm import DBM

if __name__ == "__main__":
    dbm = DBM()
    server = Server(dbm)
    server.init("109.228.49.243", 1337)
    server.listen()
    
