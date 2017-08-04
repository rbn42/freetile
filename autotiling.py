"""
TODO
"""

import setproctitle
import logging
logging.basicConfig(level=logging.DEBUG)
from helper.helper_ewmh import ewmh
from main import regularize
from util_kdtree import insert_focused_window_into_kdtree
from windowlist import windowlist
from Xlib import X, display

setproctitle.setproctitle("kdtreeautotile")

disp = display.Display()
root = disp.screen().root
# | X.SubstructureRedirectMask)
root.change_attributes(event_mask=X.SubstructureNotifyMask)

wininfo = {}

IGNORE_TYPES = [
    disp.intern_atom('_NET_WM_WINDOW_TYPE_DESKTOP'),
    disp.intern_atom('_NET_WM_WINDOW_TYPE_DOCK'),
    disp.intern_atom('_NET_WM_WINDOW_TYPE_TOOLBAR'),
    disp.intern_atom('_NET_WM_WINDOW_TYPE_MENU'),
    disp.intern_atom('_NET_WM_WINDOW_TYPE_UTILITY'),
    disp.intern_atom('_NET_WM_WINDOW_TYPE_SPLASH'),
    disp.intern_atom('_NET_WM_WINDOW_TYPE_DIALOG'),
    #    390,  # emerald
    #    391,  # volnoti
    #    348,  # docky setting
    #        disp.intern_atom('_NET_WM_WINDOW_TYPE_NORMAL'),
]
IGNORE_STATES = [
    disp.intern_atom('_NET_WM_STATE_ABOVE'),
    disp.intern_atom('_NET_WM_STATE_STICKY'),
    disp.intern_atom('_NET_WM_STATE_SKIP_TASKBAR'),
    disp.intern_atom('_NET_WM_STATE_SKIP_PAGER'),
]
IGNORE_TYPES = set(IGNORE_TYPES)
IGNORE_STATES = set(IGNORE_STATES)


# def _execute():
# import os
# os.system('python ./main.py regularize &> /dev/null')

windowlist.reset()
regularize()


def insert_window(win):
    c = win.get_wm_class()
    n = win.get_wm_name()
    s = ewmh.getWmState(win)
    t = ewmh.getWmWindowType(win)

    if len(IGNORE_STATES.intersection(s)) > 0:
        return False
    if len(IGNORE_TYPES.intersection(t)) < 0 or len(t) < 1:
        return False
    if c is not None and 'Popup' in c:
        return False

    wininfo[win.id] = c, n, t, s
    return True


for win in ewmh.getClientList():
    insert_window(win)


def add_window(win):
    for _ in range(50):
        try:
            lst = ewmh.getClientList()
        except BaseException:
            print('fail %s' % _)
            return True

    if win.id in [w.id for w in lst]:
        if insert_window(win):
            print([e.type, *wininfo[win.id]])
            windowlist.reset()
            num = len(windowlist.windowInCurrentWorkspaceInStackingOrder)
            if not regularize(force_tiling=False,
                              minimum_regularized_window=num - 1):
                return False
    return True


while True:
    e = disp.next_event()
    if e.type == X.MapNotify:
        win = e.window
        if not add_window(win):
            print('failed to add new window')
            break
    elif e.type == X.UnmapNotify:
        win = e.window
        if win.id in wininfo:
            print([e.type, *wininfo.pop(win.id)])
            windowlist.reset(ignore=[win.id])
            if len(windowlist.windowInCurrentWorkspaceInStackingOrder) < 1:
                print('no window exists')
                # quit auto tiling when no window exists.
                break
            regularize()
# Quit loop when detect overlapped windows created by user.
print('quit autotiling')

#    elif win.id in wininfo:
#        print([e.type, *wininfo[win.id]])
#        for attr in vars(X):
#            if vars(X)[attr] == e.type:
#                print(attr)
