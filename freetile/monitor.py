from .config import (bottom_padding, left_padding, right_padding, top_padding,
                     window_gap, monitors)
from .helper.helper_ewmh import ewmh


class Monitor:
    x = None
    y = None
    width = None
    height = None
    available = False

    def findMonitor(self, x0, y0, w0, h0):
        """
        find current monitor
        """
        if len(monitors) > 0:
            window = ewmh.getActiveWindow()
            if window:
                win = window.get_geometry()
                for item in monitors:
                    self.x, self.y, self.width, self.height = item

                    xin = win.x < x0 + self.x + self.width and win.x + win.width > x0 + self.x
                    yin = win.y < y0 + self.y + self.width and win.y + win.width > y0 + self.y
                    if xin and yin:
                        self.available = True
                        return self.x + x0, self.y + y0, \
                            min(self.width, w0 + x0 - self.x), \
                            min(self.height, h0 + y0 - self.y)
        self.available = False
        return x0, y0, w0, h0


monitor = Monitor()
