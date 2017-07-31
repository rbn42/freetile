import os.path
from config import EXCLUDE_APPLICATIONS, EXCLUDE_WM_CLASS, TempFile

import Xlib
from helper_ewmh import ewmh, get_window_list
from helper_xlib import disp, get_root_window_property, get_wm_class_and_state
from workarea import workarea


def initialize_windows(desktop):

    win_list = []
    win_list_all = []
    WinPosInfoAll = {}
    for win, _desktop, name in get_window_list():
        winid = win.id
        geo = win.get_geometry()
        x, y, w, h = geo.x, geo.y, geo.width, geo.height
        if not _desktop == desktop:
            continue
        if name in EXCLUDE_APPLICATIONS:
            continue

        wmclass, minimized = get_wm_class_and_state(winid)
        dock = disp.intern_atom('_NET_WM_WINDOW_TYPE_DOCK')
        if dock in ewmh.getWmWindowType(win):
            continue

        if minimized:
            continue
        wmclass = set(wmclass)
        if not wmclass == wmclass - set(EXCLUDE_WM_CLASS):
            continue

        win_list_all.append(winid)
        WinPosInfoAll[winid] = name, [int(x), int(y), w, h]

        if not (0 <= x < workarea.width and 0 <= y < workarea.height):
            continue

        win_list.append(winid)
        # TODO use xwininfo to exclude minimized windows

    return win_list, win_list_all,  WinPosInfoAll


desktop, = get_root_window_property("_NET_CURRENT_DESKTOP")
desktop_x, desktop_y, = get_root_window_property("_NET_DESKTOP_VIEWPORT")
# get_root_window_property("_NET_WORKAREA")

WinList, WinListAll, WinPosInfo = initialize_windows(desktop)
Desktop = '%s,%s,%s' % (desktop, desktop_x, desktop_y)


if os.path.exists(TempFile):
    PERSISTENT_DATA_ALL = eval(open(TempFile).read())
else:
    PERSISTENT_DATA_ALL = {}
PERSISTENT_DATA = PERSISTENT_DATA_ALL.get(Desktop, {})
OldWinList = PERSISTENT_DATA.get('winlist', [])
