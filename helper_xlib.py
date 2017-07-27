from Xlib import X, display, Xutil, protocol
from util_wmctrl import unmaximize_one
from util_xprop import get_window_frame_size

disp = display.Display()


def arrange(layout, windows, sync=True):
    for winid, lay in zip(windows, layout):
        x, y, width, height = lay
        unmaximize_one(winid, sync=False)
        move_window(winid, *lay, sync=False)
    if sync:
        disp.flush()


def move_window(windowid, x, y, w, h, sync=True):
    window_xlib = disp.create_resource_object('window', windowid)

    f_left, f_right, f_top, f_bottom = get_window_frame_size(windowid)
    w -= f_left + f_right
    h -= f_top + f_bottom

    wm_normal_hints = window_xlib.get_wm_normal_hints()
    # TODO
    print(wm_normal_hints)
    if 'Stati' in str(wm_normal_hints):
        y += f_top
        x += f_left

    window_xlib.configure(x=x, y=y, width=w, height=h)
    if sync:
        disp.flush()
