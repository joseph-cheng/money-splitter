import receipt
import pickle
from client.message_codes import MessageCode
import socket
import database
import config

class Client:
    def __init__(self):
        self.sock = None

    def init(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

        serialised_db = self.receive_message()
        self.database = pickle.loads(serialised_db)

    def deinit(self):
        self.sock.close()

    def receive_message(self, msg_len=None):
        # receives message of length msg_len, if msg_len is not specified, read 4-byte int specifying length first
        if self.sock is None:
            print("ERROR: socket not initialised when trying to receive message")
            return

        if msg_len is None:
            msg_len_bytes = self.sock.recv(4)
            msg_len = int.from_bytes(msg_len_bytes, config.endianness)

        msg_bytes = self.sock.recv(msg_len)
        return msg_bytes


    def send_message(self, msg):

        if self.sock is None:
            print("ERROR: socket not initialised when trying to send message")
            return

        msg_len_bytes = (len(msg)).to_bytes(4, config.endianness)

        self.sock.sendall(msg_len_bytes)
        self.sock.sendall(msg)

    def change_item_in_receipt(self, receipt_id, item_idx, new_item):
        msg = bytearray(MessageCode.CHANGE_ITEM_IN_RECEIPT)
        msg.extend(receipt_id.to_bytes(4, config.endianness))
        msg.extend(item_idx.to_bytes(4, config.endianness))
        msg.extend(pickle.dumps(new_item))

        self.send_message(msg)

    def add_item_to_receipt(self, receipt_id, item):
        msg = bytearray(MessageCode.ADD_ITEM_TO_RECEIPT)
        msg.extend(receipt_id.to_bytes(4, config.endianness))
        msg.extend(pickle.dumps(item))
        self.send_message(msg)

    def remove_item_from_receipt(self, receipt_id, item_idx):
        msg = bytearray(MessageCode.REMOVE_ITEM_FROM_RECEIPT)
        msg.extend(receipt_id.to_bytes(4, config.endianness))
        msg.extend(item_idx.to_bytes(4, config.endianness))
        self.send_message(msg)

    def add_receipt(self, receipt):
        msg = bytearray(MessageCode.ADD_RECEIPT)
        msg.extend(pickle.dumps(receipt))

        self.send_message(msg)

    def remove_receipt(self, receipt_id):
        msg = bytearray(MessageCode.REMOVE_RECEIPT)
        msg.extend(receipt_id.to_bytes(4, config.endianness))

        self.send_message(msg)

    def update_receipt(self, new_receipt):
        msg = bytearray(MessageCode.UPDATE_RECEIPT)
        msg.extend(pickle.dumps(new_receipt))
        self.send_message(msg)

    def save(self):
        msg = bytearray(MessageCode.SAVE_TO_DISK)
        self.send_message(msg)

    def gen_receipt_id(self):
        msg = bytearray(MessageCode.GEN_RECEIPT_ID)
        self.send_message(msg)
        rid_bytes = self.receive_message()
        rid = int.from_bytes(rid_bytes, config.endianness)

        return rid
