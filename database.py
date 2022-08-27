import logging

class Database:

    def __init__(self):
        self.receipts = {}

    def get_max_receipt_id(self):
        return max(self.receipts.keys(), default=-1)

    def change_item_in_receipt(self, receipt_id, item_idx, new_item):
        receipt_to_change = self.get_receipt_by_id(receipt_id)
        if receipt_to_change is None:
            logging.error(f"Attempting to change nonexistent receipt with ID {receipt_id}")
            return
        receipt_to_change.update_item(new_item, item_idx)


    def add_item_to_receipt(self, receipt_id, new_item, idx=None):
        receipt_to_change = self.get_receipt_by_id(receipt_id)
        if receipt_to_change is None:
            logging.error(f"Attempting to change nonexistent receipt with ID {receipt_id}")
            return
        receipt_to_change.add_item(new_item, idx=idx)


    def remove_item_from_receipt(self, receipt_id, item_idx):
        receipt_to_change = self.get_receipt_by_id(receipt_id)
        if receipt_to_change is None:
            logging.error(f"Attempting to change nonexistent receipt with ID {receipt_id}")
            return
        receipt_to_change.remove_item(item_idx)


    def update_receipt(self, receipt):
        if not(self.check_receipt_exists(receipt.id)):
            logging.error("Updating receipt that does not already exist")
            return
        self.receipts[receipt.id] = receipt




    def add_receipt(self, receipt):
        if self.check_receipt_exists(receipt.id):
            logging.warning("Sent receipt with existing receipt ID. updaing receipt instead")
            self.update_receipt(receipt)
            return
        self.receipts[receipt.id] = receipt


    def remove_receipt(self, receipt_id):
        if self.check_receipt_exists(receipt_id):
            del self.receipts[receipt_id]
        else:
            logging.error(f"Attempting to delete nonexistent receipt with ID {receipt_id}")
            return


    def check_receipt_exists(self, receipt_id):
        return receipt_id in self.receipts


    def get_receipt_by_id(self, receipt_id):
        if receipt_id in self.receipts:
            return self.receipts[receipt_id]
        else:
            logging.error(f"Receipt ID {receipt_id} not in database, returning None")
            return None

    def get_all_receipts(self):
        return list(self.receipts.values())

    def to_json(self):
        return {rid: self.receipts[rid].to_json() for rid in self.receipts}

