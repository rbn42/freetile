"""
TODO
"""
import setproctitle
setproctitle.setproctitle("kdtreeautotile")

import Xlib
from Xlib import X, display, Xutil, protocol
import os
import ewmh
ewmh = ewmh.EWMH()
disp = display.Display()
root = disp.screen().root
root.change_attributes(event_mask=X.SubstructureNotifyMask)

IGNORE_TYPES = [
    disp.intern_atom('_NET_WM_WINDOW_TYPE_DESKTOP'),
    disp.intern_atom('_NET_WM_WINDOW_TYPE_DOCK'),
    disp.intern_atom('_NET_WM_WINDOW_TYPE_TOOLBAR'),
    disp.intern_atom('_NET_WM_WINDOW_TYPE_MENU'),
    disp.intern_atom('_NET_WM_WINDOW_TYPE_UTILITY'),
    disp.intern_atom('_NET_WM_WINDOW_TYPE_SPLASH'),
    disp.intern_atom('_NET_WM_WINDOW_TYPE_DIALOG'),
    390,  # emerald
    391,  # volnoti
    348,  # docky setting
    #        disp.intern_atom('_NET_WM_WINDOW_TYPE_NORMAL'),
]
ALLOW_TYPES = [
    disp.intern_atom('_NET_WM_WINDOW_TYPE_NORMAL'),
]
print(IGNORE_TYPES)
IGNORE_TYPES = set(IGNORE_TYPES)
ALLOW_TYPES = set(ALLOW_TYPES)


os.system('python ./main.py layout regularize &> /dev/null')
while True:
    e = disp.next_event()
    if e.type in (
            X.UnmapNotify,
            X.MapNotify,
            # X.ReparentNotify,
            # X.DestroyNotify
    ):
        win = e.window
        try:
            c = win.get_wm_class()
            n = win.get_wm_name()
            t = ewmh.getWmWindowType(win)
            print([e.type, n, c, t, ])
            if len(ALLOW_TYPES.intersection(t)) < 1 or len(set(t) - ALLOW_TYPES) > 0:
                print('continue%s' % str(t))
                continue
            if not None == c and 'Popup' in c:
                print('continue%s' % str(c))
                continue
            if 'rofi' == n:
                print('continue%s' % n)
                continue
        except Xlib.error.BadWindow:
            print("error%s" % e.type)
            continue
        print('excute')
        os.system('python ./main.py layout regularize &> /dev/null')
#        for _ in range(disp.pending_events()):
#            disp.next_event()
