import os.path
import time
def lock(_file, wait=0.5):
    t0 = 0
    if os.path.exists(_file):
        t0 = float(open(_file).read())
    t1 = time.time()
    if t1 < t0 + wait:
        return False
    f = open(_file, 'w')
    f.write(str(t1))
    f.close()
    return True



def unlock(_file):
    os.remove(_file)