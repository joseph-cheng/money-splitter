#just a wrapper around database that keeps track of which receipts are new or changed
class DBM:
    def __init__(self, database, client):
        self.database = database
        self.client = client
        self.new_receipt_ids = set()
        self.changed_receipt_ids = set()
        self.removed_receipt_ids = set()

    def update_receipt(self, receipt):
        self.database.update_receipt(receipt)
        self.changed_receipt_ids.add(receipt.id)

    def add_receipt(self, receipt):
        self.database.add_receipt(receipt)
        self.new_receipt_ids.add(receipt.id)

    def remove_receipt(self, receipt_id):
        self.database.remove_receipt(receipt_id)
        self.removed_receipt_ids.add(receipt_id)

    def get_all_receipts(self):
        return self.database.get_all_receipts()


    


