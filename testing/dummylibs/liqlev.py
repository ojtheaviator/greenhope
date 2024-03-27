import time

def isSubmerged(pin):
    if (time.time() + pin) % 60 < 30:
        return(True)
    else:
        return(False)
