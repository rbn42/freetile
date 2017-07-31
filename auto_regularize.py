"""
TODO
"""
from Xlib import X, display, Xutil, protocol
import os
disp = display.Display()
root = disp.screen().root
root.change_attributes(event_mask=X.SubstructureNotifyMask)

while True:
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
