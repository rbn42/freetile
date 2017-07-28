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


from execute import execute_and_output
from config import EXCLUDE_APPLICATIONS, EXCLUDE_WM_CLASS, COMPIZ0_8
import re
from helper_xlib import get_wm_class_and_state

r_wmctrl_lG = '^([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)(\s+(.*))?$'


def initialize_windows(desktop):
    cmd = "xdpyinfo | grep 'dimension' | awk -F: '{ print $2 }' | awk '{ print $1 }' "
    s = execute_and_output(cmd)
    x, y = s.split('x')
    resx, resy = int(x), int(y)

    win_output = execute_and_output("wmctrl -lG").strip().split("\n")

    win_list = []
    win_list_all = []
    WinPosInfoAll = {}
    for win in win_output:
        _init = re.findall(r_wmctrl_lG, win)[0]
        winid, _desktop, x, y, w, h, host, _, name = _init

        if not int(_desktop) == desktop:
            continue
        # if host == 'N/A':
        #    continue
        if name in EXCLUDE_APPLICATIONS:
            continue

        winid, x, y, w, h = int(winid, 16), int(x), int(y), int(w), int(h)
        if COMPIZ0_8:
            x, y = x / 2, y / 2

        
        wmclass, minimized = get_wm_class_and_state(winid)
        if minimized:
            continue
        wmclass = set(wmclass)
        if not wmclass == wmclass - set(EXCLUDE_WM_CLASS):
            continue

        win_list_all.append(winid)
        WinPosInfoAll[winid] = name, [int(x), int(y), w, h]

        if x < 0 or x >= resx or y < 0 or y >= resy:
            continue

        win_list.append(winid)
        # TODO use xwininfo to exclude minimized windows

    return win_list, win_list_all,  WinPosInfoAll
