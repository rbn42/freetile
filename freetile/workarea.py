import math
from .config import (bottom_padding, left_padding, right_padding, top_padding,
                     window_gap)

from .helper.helper_ewmh import ewmh


class WorkArea:
    x = None
    y = None
    width = None
    height = None

    def __init__(self):
        x, y, w, h = ewmh.getWorkArea()[:4]
        self.width = w - left_padding - right_padding
        self.height = h - top_padding - bottom_padding
        self.x = x + left_padding
        self.y = y + top_padding

    def tile(self, wincount):
        # for rotated screen
        cols = 1 if workarea.width < workarea.height else 2
        layout = []
        colwidth = int((self.width + window_gap) / cols) - window_gap
        windowsleft = wincount
        x = self.x
        for col in range(cols):
            if col == cols - 1:
                colwidth = self.width + self.x - x
            rows = min(int(math.ceil(float(wincount) / cols)), windowsleft)
            windowsleft -= rows
            rowheight = int((window_gap + self.height) / rows) - window_gap
            y = self.y
            for row in range(rows):
                if row == rows - 1:
                    rowheight = self.height + self.y - y
                layout.append([x, y, colwidth, rowheight])
                y += rowheight + window_gap
            x += colwidth + window_gap

        return layout[:wincount]

    def windowInCurrentViewport(self, geo, threshold=1 / 2):
        _threshold = geo.width * threshold
        if _threshold > self.width - geo.x:
            return False
        if _threshold > geo.x + geo.width - self.x:
            return False
        _threshold = geo.height * threshold
        if _threshold > self.height - geo.y:
            return False
        if _threshold > geo.y + geo.height - self.y:
            return False
        return True


workarea = WorkArea()
