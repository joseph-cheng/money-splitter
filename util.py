import logging

def is_float(num):
    if num == "":
        return True
    try:
        float(num)
        return True
    except:
        return False

def setup_logging(log_name):
    logging.basicConfig(
            format="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
            level=logging.DEBUG,
            filename=log_name,
            )
