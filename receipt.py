class Receipt:

    ID_CTR = 0

    @staticmethod
    def gen_id():
        ret = Receipt.ID_CTR
        Receipt.ID_CTR += 1
        return ret

    def __init__(self, items, payer, date, metadata):
        self.id = Receipt.gen_id()
        self.items = items
        self.date = date
        self.payer = payer
        self.metadata = metadata

    def update_item(self, new_item, idx):
        self.items[idx] = new_item

    def remove_item(self, idx):
        self.items.pop(idx)

    def add_item(self, item, idx=None):
        if idx is None:
            self.items.append(item)
        else:
            self.items.insert(item, idx)

    def get_total_price(self):
        return sum((item.get_total_price() for item in self.items))


class ReceiptItem:

    def __init__(self, name, price, quantity, sharers):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.sharers = sharers

    def get_total_price(self):
        return self.price * self.quantity

    def get_price_for_sharer(self, sharer):
        return self.sharers.get(sharer, 0) * self.get_total_price()


