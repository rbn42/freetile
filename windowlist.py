from config import (EXCLUDE_APPLICATIONS, EXCLUDE_WM_CLASS, MIN_WINDOW_HEIGHT,
                    MIN_WINDOW_WIDTH)

from helper.ewmh import ewmh, get_window_list
from helper.xlib import (disp, get_frame_extents, get_root_window_property,
                         get_wm_class_and_state)
from workarea import workarea


class WindowList:
    windowInCurrentWorkspaceInStackingOrder = []
    windowPostion = {}
    windowName = {}
    minGeometry = {}
    ewmhactive = None

    def reset(self, ignore=[]):
        # get_root_window_property("_NET_CURRENT_DESKTOP")
        desktop = ewmh.getCurrentDesktop()
        self.ewmhactive = ewmh.getActiveWindow()
        self.windowInCurrentWorkspaceInStackingOrder = []
        self.windowName = {}
        self.windowPostion = {}
        self.minGeometry = {}

        for win, _desktop, name in get_window_list(ignore):
            winid = win.id
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
            f_left, f_right, f_top, f_bottom = get_frame_extents(winid)
            minw = max(MIN_WINDOW_WIDTH, wnh.min_width + f_left, f_right)
            minh = max(MIN_WINDOW_HEIGHT, wnh.min_height + f_top, f_right)
            self.minGeometry[winid] = minw, minh
            self.windowPostion[winid] = [int(x) - f_left, int(y) - f_top,
                                         w + f_left + f_right, h + f_top + f_bottom]

            self.windowInCurrentWorkspaceInStackingOrder.append(winid)

    def get_current_layout(self):
        return [self.windowPostion[_id]
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


windowlist = WindowList()
