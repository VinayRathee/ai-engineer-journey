def validateTitle(t):
    if len(t) == 0:
        return False
    return True

def validateIndex(i, maxIdx):
    if i < 0 or i > maxIdx:
        return False
    return True
