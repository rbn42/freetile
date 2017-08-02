from config import EXCLUDE_APPLICATIONS, EXCLUDE_WM_CLASS

from helper.ewmh import ewmh, get_window_list
from helper.xlib import (disp, get_frame_extents, get_root_window_property,
                         get_wm_class_and_state)
from workarea import workarea


class WindowList:
    windowInCurrentWorkspaceInStackingOrder = []
    windowInfo = {}
    ewmhactive = None

    def reset(self, ignore=[]):
        # get_root_window_property("_NET_CURRENT_DESKTOP")
        desktop = ewmh.getCurrentDesktop()
        self.ewmhactive = ewmh.getActiveWindow()
        self.windowInCurrentWorkspaceInStackingOrder = []
        self.windowInfo = {}
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

            self.windowInfo[winid] = name, [int(x), int(y), w, h]

            if not (0 <= x < workarea.width and 0 <= y < workarea.height):
                continue

            self.windowInCurrentWorkspaceInStackingOrder.append(winid)

    def get_current_layout(self):
        l = []
        for _id in self.windowInCurrentWorkspaceInStackingOrder:
            _name, _pos = self.windowInfo[_id]
            x, y, w, h = _pos
            f_left, f_right, f_top, f_bottom = get_frame_extents(_id)
            y -= f_top
            x -= f_left
            h += f_top + f_bottom
            w += f_left + f_right

            l.append([x, y, w, h])
        return l

    def get_active_window(self, allow_outofworkspace=False):
        active = self.ewmhactive
        if active is None:
            return None
        active = active.id
        if active not in self.windowInfo:
            return None
        if allow_outofworkspace:
            return active
        if active not in self.windowInCurrentWorkspaceInStackingOrder:
            return None
        return active


windowlist = WindowList()
