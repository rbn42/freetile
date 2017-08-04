from ewmh import EWMH
from Xlib import X

ewmh = EWMH()

_NET_WM_STATE_MAXIMIZED_VERT = ewmh.display.get_atom(
    '_NET_WM_STATE_MAXIMIZED_VERT')
_NET_WM_STATE_MAXIMIZED_HORZ = ewmh.display.get_atom(
    '_NET_WM_STATE_MAXIMIZED_HORZ')


def raise_window(win):
    ewmh.setActiveWindow(win)
    ewmh.display.flush()


def maximize_window(win):
    ewmh.setWmState(win, 1,
                    '_NET_WM_STATE_MAXIMIZED_VERT',
                    '_NET_WM_STATE_MAXIMIZED_HORZ')
    ewmh.display.flush()


def unmaximize_windows(winlist):
    """
    synchronized
    """
    # find maximized windows
    maximized_windows = set()
    for win in winlist:
        wmstate = ewmh.getWmState(win)
        if _NET_WM_STATE_MAXIMIZED_HORZ in wmstate:
            maximized_windows.add(win)
        elif _NET_WM_STATE_MAXIMIZED_VERT in wmstate:
            maximized_windows.add(win)

    # enable and send event
    for win in maximized_windows:
        win.change_attributes(event_mask=X.StructureNotifyMask)
        ewmh.setWmState(win, 0,
                        '_NET_WM_STATE_MAXIMIZED_VERT',
                        '_NET_WM_STATE_MAXIMIZED_HORZ')

    # flush
    ewmh.display.flush()

    # synchronize
    unmaximized_windows = set()
    while len(maximized_windows) > len(unmaximized_windows):
        e = ewmh.display.next_event()
        assert e.type == X.ConfigureNotify
        unmaximized_windows.add(e.window.id)

    # disable event
    for win in maximized_windows:
        win.change_attributes(event_mask=0)


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
