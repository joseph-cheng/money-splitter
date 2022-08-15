from enum import Enum

class MessageCode(Enum):
    CHANGE_ITEM_IN_RECEIPT = b'\x01'
    ADD_ITEM_TO_RECEIPT = b'\x02'
    REMOVE_ITEM_FROM_RECEIPT = b'\x03'
    ADD_RECEIPT = b'\x04'
    REMOVE_RECEIPT = b'\x05'
    SAVE_TO_DISK = b'\x06'
    GEN_RECEIPT_ID = b'\x07'


