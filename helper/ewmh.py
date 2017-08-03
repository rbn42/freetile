from ewmh import EWMH

ewmh = EWMH()


def raise_window(win):
    ewmh.setActiveWindow(win)
    ewmh.display.flush()


def maximize_window(win):
    ewmh.setWmState(win, 1,
                    '_NET_WM_STATE_MAXIMIZED_VERT',
                    '_NET_WM_STATE_MAXIMIZED_HORZ')
    ewmh.display.flush()

def unmaximize_window(win,flush=False):
    ewmh.setWmState(win, 0,
                    '_NET_WM_STATE_MAXIMIZED_VERT',
                    '_NET_WM_STATE_MAXIMIZED_HORZ')
    if flush:   
        ewmh.display.flush()

def get_window_list(ignore=[]):
    """
    in stacking order.
    """
    for win in ewmh.getClientListStacking():
        if win.id in ignore:
            continue
        name = ewmh.getWmName(win)
        if name is not None:
            name = name.decode('utf8')
        yield win, ewmh.getWmDesktop(win), name
