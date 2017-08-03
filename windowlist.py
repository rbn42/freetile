from config import (EXCLUDE_APPLICATIONS, EXCLUDE_WM_CLASS, MIN_WINDOW_HEIGHT,
                    MIN_WINDOW_WIDTH)

import helper.xcb
from helper.helper_ewmh import (ewmh, get_window_list, maximize_window, raise_window,
                         unmaximize_window)
from helper.xlib import (disp, get_frame_extents, get_root_window_property,
                         get_wm_class_and_state)
from workarea import workarea


class WindowList:
    windowInCurrentWorkspaceInStackingOrder = []
    windowGeometry = {}
    windowName = {}
    minGeometry = {}
    windowObjectMap = {}
    ewmhactive = None

    def maximize_window(self, winid):
        win = self.windowObjectMap[winid]
        maximize_window(win)

    def raise_window(self, winid):
        win = self.windowObjectMap[winid]
        raise_window(win)

    def reset(self, ignore=[]):
        # get_root_window_property("_NET_CURRENT_DESKTOP")
        desktop = ewmh.getCurrentDesktop()
        self.ewmhactive = ewmh.getActiveWindow()
        self.windowInCurrentWorkspaceInStackingOrder = []
        self.windowName = {}
        self.windowGeometry = {}
        self.minGeometry = {}
        self.windowObjectMap = {}

        for win, _desktop, name in get_window_list(ignore):
            winid = win.id
            self.windowObjectMap[winid] = win
            geo = win.get_geometry()
            x, y, w, h = geo.x, geo.y, geo.width, geo.height
            if not _desktop == desktop:
                continue
            if name in EXCLUDE_APPLICATIONS:
                continue

            wmclass, minimized = get_wm_class_and_state(winid)
            dock = disp.intern_atom('_NET_WM_WINDOW_TYPE_DOCK')
            if dock in ewmh.getWmWindowType(win):
                continue

            if minimized:
                continue
            wmclass = set(wmclass)
            if not wmclass == wmclass - set(EXCLUDE_WM_CLASS):
                continue

            self.windowName[winid] = name

            if not (0 <= x < workarea.width and 0 <= y < workarea.height):
                continue

            wnh = win.get_wm_normal_hints()
            f_left, f_right, f_top, f_bottom = get_frame_extents(win)
            minw = max(MIN_WINDOW_WIDTH, wnh.min_width + f_left, f_right)
            minh = max(MIN_WINDOW_HEIGHT, wnh.min_height + f_top, f_right)
            self.minGeometry[winid] = minw, minh
            self.windowGeometry[winid] = [int(x) - f_left, int(y) - f_top,
                                          w + f_left + f_right, h + f_top + f_bottom]

            self.windowInCurrentWorkspaceInStackingOrder.append(winid)

    def get_current_layout(self):
        return [self.windowGeometry[_id]
                for _id in self.windowInCurrentWorkspaceInStackingOrder]

    def get_active_window(self, allow_outofworkspace=False):
        active = self.ewmhactive
        if active is None:
            return None
        active = active.id
        if active in self.windowInCurrentWorkspaceInStackingOrder:
            return active
        if allow_outofworkspace and active in self.windowName:
            return active

    def arrange(self, layout, windowids):
        windows = [self.windowObjectMap[wid]for wid in windowids]
        # unmaximize
        for win in windows:
            unmaximize_window(win)

        # TODO need correct frame extents after maximized windows unmaximized
        # disp.flush()
        # disp.sync()
        import time
        time.sleep(0.1)

        layout_final = []
        # move windows
        for win, lay, in zip(windows, layout, ):
            normal_hints = win.get_wm_normal_hints()

            x, y, width, height = lay
            f_left, f_right, f_top, f_bottom = get_frame_extents(win)
            width -= f_left + f_right
            height -= f_top + f_bottom

            # window gravity: Static
            if normal_hints.win_gravity == 10:
                y += f_top
                x += f_left
            layout_final.append([x, y, width, height])
        return helper.xcb.arrange(layout_final, windowids)


windowlist = WindowList()
