import math
from config import (BottomPadding, LeftPadding, RightPadding, TopPadding,
                    WinBorder)

from helper.ewmh import ewmh


class WorkArea:
    x = None
    y = None
    width = None
    height = None

    def __init__(self):
        # TODO
        # get_root_window_property("_NET_WORKAREA")
        x, y, w, h = ewmh.getWorkArea()[:4]
        self.width = w - LeftPadding - RightPadding
        self.height = h - TopPadding - BottomPadding
        self.x = x + LeftPadding
        self.y = y + TopPadding

    def layout_shift(self, x, y, w, h):
        return (self.x + x + WinBorder,
                self.y + y + WinBorder,
                w - 2 * WinBorder,
                h - 2 * WinBorder)

    def tile(self, wincount):
        # for rotated screen
        cols = 1 if workarea.width < workarea.height else 2
        layout = []
        colwidth = int(self.width / cols)
        windowsleft = wincount
        for col in range(cols):
            rows = min(int(math.ceil(float(wincount) / cols)), windowsleft)
            windowsleft -= rows
            rowheight = int(self.height / rows)
            for row in range(rows):
                layout.append(self.layout_shift(
                    colwidth * col,
                    row * rowheight,
                    colwidth,
                    rowheight))
        return layout[:wincount]


workarea = WorkArea()

