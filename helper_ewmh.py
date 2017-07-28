
from ewmh import EWMH
ewmh=EWMH()
from helper_xlib import get_window

@get_window
def raise_window(win):
    ewmh.setActiveWindow(win)
    ewmh.display.flush()

def get_active_window(allow_outofworkspace=False):
    from global_variables import WinList, WinPosInfo
    active=ewmh.getActiveWindow()
    if None==active:
        return None
    active = active.id
    if active not in WinPosInfo:
        return None
    if allow_outofworkspace:
        return active
    if active not in WinList:
        return None
    return active
