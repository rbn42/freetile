"""
TODO
"""
from Xlib import X, display, Xutil, protocol
import time
import os
import ewmh
ewmh = ewmh.EWMH()
disp = display.Display()
root = disp.screen().root
root.change_attributes(event_mask=X.SubstructureNotifyMask)

#t = time.time()
while True:
    #    if time.time()-t>0.1:
    #    t = time.time()
    e = disp.next_event()
    if e.type in (
            X.UnmapNotify,
            X.MapNotify,
            # X.ReparentNotify,
            # X.DestroyNotify
    ):
        os.system('python ./main.py layout regularize &> ~/dev/null')
        print(e)
        for _ in range(disp.pending_events()):
            disp.next_event()

#            print(e.type)
        # print(e.window.id)
#                print(ewmh.getWmName(e.window))
