############################################################################
# Copyright (c) 2009   unohu <unohu0@gmail.com>                            #
#                                                                          #
# Permission to use, copy, modify, and/or distribute this software for any #
# purpose with or without fee is hereby granted, provided that the above   #
# copyright notice and this permission notice appear in all copies.        #
#                                                                          #
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES #
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF         #
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR  #
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES   #
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN    #
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF  #
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.           #
#                                                                          #
############################################################################


from config import EXCLUDE_APPLICATIONS, EXCLUDE_WM_CLASS, COMPIZ0_8
import re
from helper_xlib import get_wm_class_and_state,get_root_window_property
from helper_ewmh import get_window_list




def initialize_windows(desktop):
    minx,miny,maxx,maxy= get_root_window_property("_NET_WORKAREA")

    win_list = []
    win_list_all = []
    WinPosInfoAll = {}
    for win, _desktop, name in get_window_list():
        winid = win.id
        geo = win.get_geometry()
        x, y, w, h=geo.x,geo.y,geo.width,geo.height
        if not None==name:
            name=name.decode('utf8')

        if not _desktop == desktop:
            continue
        if name in EXCLUDE_APPLICATIONS:
            continue

        wmclass, minimized = get_wm_class_and_state(winid)
        if minimized:
            continue
        wmclass = set(wmclass)
        if not wmclass == wmclass - set(EXCLUDE_WM_CLASS):
            continue

        win_list_all.append(winid)
        WinPosInfoAll[winid] = name, [int(x), int(y), w, h]

        if not (minx<=x<maxx and miny<=y<maxy):
            continue

        win_list.append(winid)
        # TODO use xwininfo to exclude minimized windows

    return win_list, win_list_all,  WinPosInfoAll
