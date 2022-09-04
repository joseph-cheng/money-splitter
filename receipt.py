import logging

class Receipt:

    ID_CTR = 0

    @staticmethod
    def gen_id():
        ret = Receipt.ID_CTR
        Receipt.ID_CTR += 1
        return ret

    @staticmethod
    def str_to_id(id):
        try:
            return int(id)
        except:
            logging.error(f"Given id {id} cannot be converted, returning None")
            return None

    def __init__(self, payer, date, metadata=None, from_client=False, client=None):
        if from_client:
            if client == None:
                logging.error("Attempting to generate receipt on the client without access to the server")
                self.id = -Receipt.gen_id()
            else:
                self.id = client.gen_receipt_id()
                # if this happens, client is not initialised
                if self.id is None:
                    self.id = -Receipt.gen_id()


        else:
            self.id = Receipt.gen_id()
        self.items = []
        self.date = date
        self.payer = payer
        self.metadata = metadata

    def update_item(self, new_item, idx):
        self.items[idx] = new_item

    def remove_item(self, idx):
        self.items.pop(idx)

    def clear_items(self):
        self.items = []

    def add_item(self, item, idx=None):
        if idx is None:
            self.items.append(item)
        else:
            self.items.insert(item, idx)

    def get_total_price(self):
        return sum((item.get_total_price() for item in self.items))

    def to_json(self):
        return {
                "date": self.date,
                "payer": self.payer,
                "metadata": self.metadata,
                "items": [
                    item.to_json() for item in self.items
                    ],
                }


class ReceiptItem:

    def __init__(self, name, price, quantity, sharers, incomplete=False):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.sharers = sharers
        self.incomplete = incomplete

    def get_total_price(self):
        try:
            return 0 if self.incomplete else self.price * self.quantity
        except TypeError:
            return 0

    def get_price_for_sharer(self, sharer):
        return self.sharers.get(sharer, 0) * self.get_total_price()

    def to_json(self):
        return {
                "name": self.name,
                "price": self.price,
                "quantity": self.quantity,
                "sharers": self.sharers,
                "incomplete": self.incomplete,
                }


