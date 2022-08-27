from server.server import Server
from server.dbm import DBM
import util

if __name__ == "__main__":
    util.setup_logging("server.log")
    dbm = DBM()
    server = Server(dbm)
    server.init("109.228.49.243", 1337)
    server.listen()
    
