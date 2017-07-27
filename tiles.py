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

from util_xdotool import get_active_window, minimize_one, raise_window
from util_wmctrl import maximize_one

from global_variables import WinList,  OrigX, MaxHeight,     MaxWidth, OrigY
from config import WinBorder


def minimize(wincount):
    for win in WinList:
        minimize_one(win)


def maximize(wincount):
    active = get_active_window()
    for win in WinList:
        maximize_one(win)
    raise_window(active)
    return None


def get_simple_tile(wincount):
    MwFactor = 0.55
    rows = wincount - 1
    layout = []
    if rows == 0:
        layout.append(layout_shift(0, 0, MaxWidth, MaxHeight))
        return layout
    else:
        layout.append(layout_shift(0, 0, int(MaxWidth * MwFactor),
                                   MaxHeight))

    x = int((MaxWidth * MwFactor))
    width = int((MaxWidth * (1 - MwFactor)))
    height = int(MaxHeight / rows)

    for n in range(0, rows):
        y = int((MaxHeight / rows) * (n))
        layout.append(layout_shift(x, y, width, height))

    return layout

# from https://bbs.archlinux.org/viewtopic.php?id=64100&p=7 #151


def get_columns_tile(wincount, ncolumns):
    # 2nd term rounds up if num columns not a factor of
    # num windows; this leaves gaps at the bottom
    nrows = (wincount / ncolumns) + int(bool(wincount % ncolumns))

    layout = []
    x = OrigX
    y = OrigY

    height = int(MaxHeight / nrows - 2 * WinBorder)
    width = int(MaxWidth / ncolumns - 2 * WinBorder)

    for n in range(0, wincount):
        column = n % ncolumns
        row = n / ncolumns

        x = OrigX + column * width
        y = OrigY + (int((MaxHeight / nrows) * (row)))
        layout.append((x, y, width, height))

    return layout


def get_fair_tile(wincount):
    import math
    ncolumns = int(math.ceil(math.sqrt(wincount)))
    return get_columns_tile(wincount, ncolumns)
# end https://bbs.archlinux.org/viewtopic.php?id=64100&p=7 #151


def get_vertical_tile(wincount):
    layout = []
    y = OrigY
    width = int(MaxWidth / wincount)
    height = MaxHeight - 2 * WinBorder
    for n in range(0, wincount):
        x = OrigX + n * width
        layout.append((x, y, width, height))

    return layout


def get_horiz_tile(wincount):
    layout = []
    x = OrigX
    height = int(MaxHeight / wincount - 2 * WinBorder)
    width = MaxWidth
    for n in range(0, wincount):
        y = OrigY + int((MaxHeight / wincount) * (n))
        layout.append((x, y, width, height))

    return layout


# from https://bbs.archlinux.org/viewtopic.php?id=64100&p=6  #150
import math


def get_autogrid_tile(wincount):
    layout = []
    rows = int(math.floor(math.sqrt(wincount)))
    rowheight = int(MaxHeight / rows)
    windowsleft = wincount
    for row in range(rows):
        cols = min(int(math.ceil(float(wincount) / rows)), windowsleft)
        windowsleft -= cols
        colwidth = MaxWidth / cols
        for col in range(cols):
            layout.append(layout_shift(colwidth * col, row *
                                       rowheight, colwidth, rowheight))
    return layout[:wincount]
# end https://bbs.archlinux.org/viewtopic.php?id=64100&p=6  #150


def get_columns_tile2(wincount, reverse=False, cols=2):
    if wincount < 2:
        return get_vertical_tile(wincount)
    layout = []
    colwidth = int(MaxWidth / cols)
    windowsleft = wincount
    if reverse:
        _range = range(cols - 1, -1, -1)
    else:
        _range = range(cols)
    for col in _range:
        rows = min(int(math.ceil(float(wincount) / cols)), windowsleft)
        windowsleft -= rows
        rowheight = int(MaxHeight / rows)
        for row in range(rows):
            layout.append(layout_shift(
                colwidth * col,
                row * rowheight,
                colwidth,
                rowheight))
    return layout[:wincount]


def get_columns_tile3(wincount, reverse=False,  column_num=2):
    if wincount < 2:
        return get_vertical_tile(wincount)

    column_num = min(wincount, column_num)
    cols = []
    for _ in range(column_num):
        cols.append([])

    for i in range(wincount):
        if reverse:
            cols[(-1 - i) % column_num].append(i)
        else:
            cols[i % column_num].append(i)

    layout = []
    colwidth = int(MaxWidth / column_num)
    for col in range(column_num):
        rows = len(cols[col])
        rowheight = MaxHeight / rows
        for row in range(rows):
            layout.append(layout_shift(
                colwidth * col,
                row * rowheight,
                colwidth,
                rowheight))
    return layout  # [:wincount]


def layout_shift(x, y, w, h):
    return (OrigX + x + WinBorder,
            OrigY + y + WinBorder,
            w - 2 * WinBorder,
            h - 2 * WinBorder)
