def cleanStr(s):
    if not s:
        return ""
    return s.strip()

def idGen():
    import random
    return random.randint(1000, 9999)
