from .config import (
    bottom_padding,
    left_padding,
    right_padding,
    top_padding,
    window_gap,
)
from .helper.helper_ewmh import ewmh

import subprocess
import re


class Monitor:
    x = None
    y = None
    width = None
    height = None
    available = False

    def findMonitor(self, xywh0):
        """
        find current monitor
        """
        s = subprocess.check_output('xrandr').decode()
        l = re.findall('(\d+)x(\d+)\+(\d+)\+(\d+)', s)
        monitors = [(int(x), int(y), int(w), int(h)) for w, h, x, y in l]
        if len(monitors) > 0:
            window = ewmh.getActiveWindow()
            if window:
                win = window.get_geometry()
                for item in monitors:
                    self.x, self.y, self.width, self.height = item
                    if xywh0 is None:
                        return (0, 0, self.width, self.height)
                    x0, y0, w0, h0 = xywh0

                    xin = win.x < x0 + self.x + self.width and win.x + win.width > x0 + self.x
                    yin = win.y < y0 + self.y + self.width and win.y + win.width > y0 + self.y
                    if xin and yin:
                        self.available = True and len(monitors) > 2
                        if (self.x < 1 and self.y < 1):
                            return self.x + x0, self.y + y0, w0, h0
                        else:
                            return self.x + x0, self.y + y0, \
                            min(self.width, w0 + x0 - self.x), \
                            min(self.height, h0 + y0 - self.y)
        self.available = False
        return x0, y0, w0, h0


monitor = Monitor()
