import pickle
import database
from threading import Lock

class DBM:

    def __init__(self, dbfilename=None):
        if dbfilename is None:
            dbfile = open("default.db", "w+")
            self.dbfilename = "default.db"
            self.database = database.Database()
        else:
            dbfile = open(dbfilename, "w+")
            self.dbfilename = dbfilename
            self.database = pickle.load(dbfile)

        dbfile.close()

        self.db_lock = Lock()


    def change_item_in_receipt(self, receipt_id, item_idx, new_item):
        with self.db_lock:
            self.database.change_item_in_receipt(receipt_id, item_idx, new_item)

    def add_item_to_receipt(self, receipt_id, new_item, idx=None):
        with self.db_lock:
            self.database.add_item_to_receipt(receipt_id, new_item, idx=idx)


    def remove_item_from_receipt(self, receipt_id, item_idx):
        with self.db_lock:
            self.database.remove_item_from_receipt(receipt_id, item_idx)

    def update_receipt(self, receipt):
        with self.db_lock:
            self.database.update_receipt(receipt)




    def add_receipt(self, receipt):
        with self.db_lock:
            self.database.add_receipt(receipt)


    def remove_receipt(self, receipt_id):
        with self.db_lock:
            self.database.remove_receipt(receipt_id)

    def save(self):
        with self.db_lock:
            with open(self.dbfilename, "w+") as f:
                pickle.dump(self.database, f)

    def serialise_db(self):
        with self.db_lock:
            return pickle.dumps(self.database)






