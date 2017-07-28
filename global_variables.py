import os.path
from initialize import initialize_windows
from helper_xlib import get_root_window_property
from config import BottomPadding, RightPadding, LeftPadding, TopPadding,\
    TempFile

desktop, =get_root_window_property("_NET_CURRENT_DESKTOP")
desktop_x, desktop_y, =get_root_window_property("_NET_DESKTOP_VIEWPORT")
OrigXstr, OrigYstr, MaxWidthStr, MaxHeightStr = get_root_window_property("_NET_WORKAREA")

WinList, WinListAll, WinPosInfo = initialize_windows(desktop)
Desktop = '%s,%s,%s' % (desktop, desktop_x, desktop_y)

MaxWidth = int(MaxWidthStr) - LeftPadding - RightPadding
MaxHeight = int(MaxHeightStr) - TopPadding - BottomPadding
OrigX = int(OrigXstr) + LeftPadding
OrigY = int(OrigYstr) + TopPadding

if os.path.exists(TempFile):
    PERSISTENT_DATA_ALL = eval(open(TempFile).read())
else:
    PERSISTENT_DATA_ALL = {}
PERSISTENT_DATA = PERSISTENT_DATA_ALL.get(Desktop, {})
OldWinList = PERSISTENT_DATA.get('winlist', [])
