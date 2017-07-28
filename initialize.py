from config import EXCLUDE_APPLICATIONS, EXCLUDE_WM_CLASS
from helper_xlib import get_wm_class_and_state, get_root_window_property,disp
from helper_ewmh import get_window_list,ewmh
import Xlib



def initialize_windows(desktop):
    minx, miny, maxx, maxy = get_root_window_property("_NET_WORKAREA")
    minx=miny=0

    win_list = []
    win_list_all = []
    WinPosInfoAll = {}
    for win, _desktop, name in get_window_list():
        winid = win.id
        geo = win.get_geometry()
        x, y, w, h = geo.x, geo.y, geo.width, geo.height
        if not None == name:
            name = name.decode('utf8')

        if not _desktop == desktop:
            continue
        if name in EXCLUDE_APPLICATIONS:
            continue

        wmclass, minimized = get_wm_class_and_state(winid)
        dock=disp.intern_atom('_NET_WM_WINDOW_TYPE_DOCK')
        if dock in ewmh.getWmWindowType(win):
            continue

        if minimized:
            continue
        wmclass = set(wmclass)
        if not wmclass == wmclass - set(EXCLUDE_WM_CLASS):
            continue

        win_list_all.append(winid)
        WinPosInfoAll[winid] = name, [int(x), int(y), w, h]

        if not (minx <= x < maxx and miny <= y < maxy):
            continue

        win_list.append(winid)
        # TODO use xwininfo to exclude minimized windows

    return win_list, win_list_all,  WinPosInfoAll
