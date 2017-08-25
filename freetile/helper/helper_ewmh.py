from ewmh import EWMH
from Xlib import X

ewmh = EWMH()

_NET_WM_STATE_MAXIMIZED_VERT = ewmh.display.get_atom(
    '_NET_WM_STATE_MAXIMIZED_VERT')
_NET_WM_STATE_MAXIMIZED_HORZ = ewmh.display.get_atom(
    '_NET_WM_STATE_MAXIMIZED_HORZ')
_NET_WM_STATE_FULLSCREEN = ewmh.display.get_atom('_NET_WM_STATE_FULLSCREEN')


def raise_window(win):
    ewmh.setActiveWindow(win)
    ewmh.display.flush()


def maximize_window(win, sync=True, flush=True):
    if not sync:
        ewmh.setWmState(win, 1,
                        '_NET_WM_STATE_MAXIMIZED_VERT',
                        '_NET_WM_STATE_MAXIMIZED_HORZ')
        if flush:
            ewmh.display.flush()
    else:
        wmstate = set(ewmh.getWmState(win))
        if len({_NET_WM_STATE_MAXIMIZED_HORZ,
                _NET_WM_STATE_MAXIMIZED_VERT} - wmstate) < 1:
            return
        win.change_attributes(event_mask=X.StructureNotifyMask)
        ewmh.setWmState(win, 1,
                        '_NET_WM_STATE_MAXIMIZED_VERT',
                        '_NET_WM_STATE_MAXIMIZED_HORZ')
        ewmh.display.flush()
        timeout = 10
        for _ in range(timeout):
            e = ewmh.display.next_event()
            if e.type == X.ConfigureNotify:
                if e.window.id == win.id:
                    break
        win.change_attributes(event_mask=0)


def unmaximize_windows(winlist):
    """
    synchronized
    """
    # find maximized windows
    maximized_windows = set()
    for win in winlist:
        wmstate = ewmh.getWmState(win)
        if not {_NET_WM_STATE_MAXIMIZED_HORZ,
                _NET_WM_STATE_MAXIMIZED_VERT,
                _NET_WM_STATE_FULLSCREEN}.isdisjoint(wmstate):
            maximized_windows.add(win)

    # enable and send event
    for win in maximized_windows:
        win.change_attributes(event_mask=X.StructureNotifyMask)
        ewmh.setWmState(win, 0,
                        '_NET_WM_STATE_MAXIMIZED_VERT',
                        '_NET_WM_STATE_MAXIMIZED_HORZ',)
        ewmh.setWmState(win, 0,
                        '_NET_WM_STATE_FULLSCREEN',)

    # flush
    ewmh.display.flush()

    # synchronize
    unmaximized_windows = set()
    timeout = len(maximized_windows) * 10
    for _ in range(timeout):
        if not len(maximized_windows) > len(unmaximized_windows):
            break
        e = ewmh.display.next_event()
        if e.type == X.ConfigureNotify:
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
