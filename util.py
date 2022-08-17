def is_float(num):
    if num == "":
        return True
    try:
        float(num)
        return True
    except:
        return False
