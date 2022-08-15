from receipt import Receipt
import config
import pickle
from client.message_codes import MessageCode
import threading

class ClientHandler(threading.Thread):

    def __init__(self, sock, dbm):
        threading.Thread.__init__(self)
        self.sock = sock
        self.dbm = dbm

    def run(self):
        print("INFO: thread started to handle client...")
        print("INFO: sending database to client...")
        # first send client our database for them to update to
        serialised_db = self.dbm.serialise_db()
        serialised_db_size_bytes = (len(serialised_db)).to_bytes(4, config.endianness)
        self.sock.sendall(serialised_db_size_bytes)
        self.sock.sendall(serialised_db)
        received_data = bytearray()
        next_message_len = 9e99
        while True:
            received_data.extend(self.sock.recv(4096))

            if len(received_data) >= 4:
                next_message_len = int.from_bytes(received_data[:4], config.endianness)

            if len(received_data) >= 4 + next_message_len:
                message_to_process = received_data[4:4 + next_message_len]
                process_message(self, msg)
                received_data = received_data[4+next_message_len:]
        print("INFO: client exited...")

    def process_message(self, msg):
        if msg[0] == CHANGE_ITEM_IN_RECEIPT:
            self.handle_change_item_in_receipt(msg)
            
        elif msg[0] == ADD_ITEM_TO_RECEIPT:
            self.handle_add_item_to_receipt(msg)

        elif msg[0] == REMOVE_ITEM_FROM_RECEIPT:
            self.handle_remove_item_from_receipt(msg)

        elif msg[0] == ADD_RECEIPT:
            self.handle_add_receipt(msg)

        elif msg[0] == REMOVE_RECEIPT:
            self.handle_remove_receipt(msg)

        elif msg[0] == SAVE_TO_DISK:
            self.handle_save(msg)


    def handle_change_item_in_receipt(self, msg):
        msg_code = msg[0]
        if msg_code != MessageCode.CHANGE_ITEM_IN_RECEIPT:
            print(f"ERROR: handling incorrect message {msg}")
            return


        # 4 bytes for receipt id
        receipt_id_bytes = msg[1:1+4]
        # 4 bytes for item idx
        item_idx_bytes = msg[5:5+4]

        item_bytes = msg[9:]

        receipt_id = int.from_bytes(receipt_id_bytes, config.endianness)
        item_idx = int.from_bytes(item_idx_bytes, config.endianness)
        item = pickle.loads(item_bytes)

        self.dbm.change_item_in_receipt(receipt_id, item_idx, item)

    def handle_add_item_to_receipt(self, msg):
        msg_code = msg[0]
        if msg_code != MessageCode.ADD_ITEM_TO_RECEIPT:
            print(f"ERROR: handling incorrect message {msg}")
            return

        receipt_id_bytes = msg[1:1+4]
        item_bytes = msg[5:]
        
        receipt_id = int.from_bytes(receipt_id_bytes, config.endianness)
        item = pickle.loads(item_bytes)

        self.dbm.add_item_to_receipt(self, receipt_id, item)

    def handle_remove_item_from_receipt(self, msg):
        msg_code = msg[0]
        if msg_code != MessageCode.REMOVE_ITEM_FROM_RECEIPT:
            print(f"ERROR: handling incorrect message {msg}")
            return

        receipt_id_bytes = msg[1:1+4]
        item_idx_bytes = msg[5:5+4]

        receipt_id = int.from_bytes(receipt_id_bytes, config.endianness)
        item_idx = int.from_bytes(item_idx_bytes, config.endianness)

        self.dbm.remove_item_from_receipt(receipt_id, item_idx)

    def handle_add_receipt(self, msg):
        msg_code = msg[0]
        if msg_code  != MessageCode.ADD_RECEIPT:
            print(f"ERROR: handling incorrect message {msg}")
            return

        receipt_bytes  = msg[1:]
        receipt = pickle.loads(receipt_bytes)

        self.dbm.add_receipt(receipt)

    def handle_remove_receipt(self, msg):
        msg_code = msg[0]
        if msg_code != MessageCode.REMOVE_RECEIPT:
            print(f"ERROR: handling incorrect message {msg}")
            return

        receipt_id_bytes = msg[1:1+4]

        receipt_id = int.from_bytes(receipt_id_bytes, config.endianness)

        self.dbm.remove_receipt(receipt_id)

    def handle_save(self, msg):
        msg_code = msg[0]
        if msg_code != MessageCode.SAVE_TO_DISK:
            print(f"ERROR: handling incorrect message {msg}")
            return

        self.dbm.save()

    def handle_gen_receipt_id(self, msg):
        msg_code = msg[0]
        if msg_code != MessageCode.GEN_RECEIPT_ID:
            print(f"ERROR: handling incorrect message {msg}")
            return

        rid = Receipt.gen_id()
        rid_bytes = rid.to_bytes(4, config.endianness)

        self.sock.send(rid_bytes)


