import logging
import pickle
from client.message_codes import MessageCode
import socket
import config
from client.dbm import DBM

class Client:
    def __init__(self):
        self.sock = None
        self.dbm = None
        self.initialised = False
        self.byte_buffer = bytearray()

    def init(self, ip, port):
        if self.initialised:
            logging.warning("Trying to initialise already initialised socket")
            return
        logging.info(f"Attempting to connect to {ip}:{port}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.initialised = True

    def download_db(self):
        serialised_db = self.receive_message()
        database = pickle.loads(serialised_db)
        self.dbm = DBM(database, self)

    def deinit(self):
        if not(self.initialised):
            logging.warning("Trying to deinitialise non-initialised socket")
            return
        self.sock.close()
        self.initialised = False


    def receive_message_known_length(self, msg_len):
        if not(self.initialised):
            logging.error("Trying to receive message from non-initialised socket")
            return None
        # receives message of length msg_len, if msg_len is not specified, read 4-byte int specifying length first
        if self.sock is None:
            logging.error("Socket not initialised when trying to receive message")
            return


        while len(self.byte_buffer) < msg_len:
            bytes_received = self.sock.recv(4096)
            logging.info(f"Received {len(bytes_received)} bytes")
            self.byte_buffer.extend(bytes_received)

        ret = self.byte_buffer[:msg_len]
        self.byte_buffer = self.byte_buffer[msg_len:]
        return ret


    def receive_message(self, msg_len=None):
        if msg_len is None:
            msg_len_bytes = self.receive_message_known_length(4)
            msg_len = int.from_bytes(msg_len_bytes, byteorder=config.endianness)

        return self.receive_message_known_length(msg_len)


    def send_message(self, msg):
        if not(self.initialised):
            logging.error("Trying to send message to non-initialised socket")
            return

        if self.sock is None:
            logging.error("Socket not initialised when trying to send message")
            return

        msg_len_bytes = (len(msg)).to_bytes(4, config.endianness)

        self.sock.sendall(msg_len_bytes)
        self.sock.sendall(msg)

    def change_item_in_receipt(self, receipt_id, item_idx, new_item):
        msg = bytearray(MessageCode.CHANGE_ITEM_IN_RECEIPT.value)
        msg.extend(receipt_id.to_bytes(4, config.endianness))
        msg.extend(item_idx.to_bytes(4, config.endianness))
        msg.extend(pickle.dumps(new_item))

        self.send_message(msg)

    def add_item_to_receipt(self, receipt_id, item):
        msg = bytearray(MessageCode.ADD_ITEM_TO_RECEIPT.value)
        msg.extend(receipt_id.to_bytes(4, config.endianness))
        msg.extend(pickle.dumps(item))
        self.send_message(msg)

    def remove_item_from_receipt(self, receipt_id, item_idx):
        msg = bytearray(MessageCode.REMOVE_ITEM_FROM_RECEIPT.value)
        msg.extend(receipt_id.to_bytes(4, config.endianness))
        msg.extend(item_idx.to_bytes(4, config.endianness))
        self.send_message(msg)

    def add_receipt(self, receipt):
        msg = bytearray(MessageCode.ADD_RECEIPT.value)
        msg.extend(pickle.dumps(receipt))

        self.send_message(msg)

    def remove_receipt(self, receipt_id):
        msg = bytearray(MessageCode.REMOVE_RECEIPT.value)
        msg.extend(receipt_id.to_bytes(4, config.endianness))

        self.send_message(msg)

    def update_receipt(self, new_receipt):
        msg = bytearray(MessageCode.UPDATE_RECEIPT.value)
        msg.extend(pickle.dumps(new_receipt))
        self.send_message(msg)

    def save(self):
        msg = bytearray(MessageCode.SAVE_TO_DISK.value)
        self.send_message(msg)

    def gen_receipt_id(self):
        msg = bytearray(MessageCode.GEN_RECEIPT_ID.value)
        self.send_message(msg)
        rid_bytes = self.receive_message(msg_len=4)
        if rid_bytes is None:
            return None
        rid = int.from_bytes(rid_bytes, config.endianness)

        return rid

    def upload_changes(self):
        for receipt_id in self.dbm.new_receipt_ids:
            self.add_receipt(self.dbm.get_receipt_by_id(receipt_id))


        for receipt_id in self.dbm.changed_receipt_ids:
            self.update_receipt(self.dbm.get_receipt_by_id(receipt_id))


        for receipt_id in self.dbm.removed_receipt_ids:
            self.remove_receipt(receipt_id)

        self.dbm.removed_receipt_ids = set()
        self.dbm.changed_receipt_ids = set()
        self.dbm.new_receipt_ids = set()

        self.save()
