"""
TODO
"""
from Xlib import X, display, Xutil, protocol
import time
import os
disp = display.Display()
t=time.time()
while True:
    if time.time()-t>0.1:
        t=time.time()
        e = disp.next_event()
        if e.type in (X.MappingNotify,X.UnmapNotify):
            os.system('python ./main.py layout regularize')
            print(e.type)
