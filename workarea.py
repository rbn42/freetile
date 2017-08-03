import math
from config import (BottomPadding, LeftPadding, RightPadding, TopPadding,
                    WindowGap)

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

    def tile(self, wincount):
        # for rotated screen
        cols = 1 if workarea.width < workarea.height else 2
        layout = []
        colwidth = int((self.width + WindowGap) / cols) - WindowGap
        windowsleft = wincount
        x = self.x
        for col in range(cols):
            if col == cols - 1:
                colwidth = self.width - x
            rows = min(int(math.ceil(float(wincount) / cols)), windowsleft)
            windowsleft -= rows
            rowheight = int((WindowGap + self.height) / rows) - WindowGap
            y = self.y
            for row in range(rows):
                if row == rows - 1:
                    rowheight = self.height - y
                layout.append([x, y, colwidth, rowheight])
                y += rowheight + WindowGap
            x += colwidth + WindowGap

        return layout[:wincount]


workarea = WorkArea()
