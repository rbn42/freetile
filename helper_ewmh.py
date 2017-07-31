
from ewmh import EWMH
from helper_xlib import get_window

ewmh = EWMH()


@get_window
def raise_window(win):
    ewmh.setActiveWindow(win)
    ewmh.display.flush()


def get_window_list():
    """
    in stacking order.
    """
    for win in ewmh.getClientListStacking():
        name = ewmh.getWmName(win)
        if name is not None:
            name = name.decode('utf8')
        yield win, ewmh.getWmDesktop(win), name


def get_active_window(allow_outofworkspace=False):
    from global_variables import WinList, WinPosInfo
    active = ewmh.getActiveWindow()
    if None == active:
        return None
    active = active.id
    if active not in WinPosInfo:
        return None
    if allow_outofworkspace:
        return active
    if active not in WinList:
        return None
    return active
