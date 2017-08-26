from . import config
import logging

from .helper import emacs
from .helper import vim
from .util_kdtree import (find_kdtree, move_kdtree,
                          regularize_or_insert_windows, resize_kdtree)
from .windowlist import windowlist
from .workarea import workarea


def regularize(force_tiling=True, minimum_regularized_window=None):
    '''
    Try to regularize windows or add a new window into the K-D tree.
    '''
    logging.info('regularize layout')
    stack = windowlist.windowInCurrentWorkspaceInStackingOrder
    num = len(stack)
    if num == 0:
        pass
    elif num == 1:
        windowlist.maximize_window(stack[0])
    else:
        """
        Allow to insert 1/3 new windows to a regularized layout of the rest 2/3 windows.
        """
        if minimum_regularized_window is None:
            minimum_regularized_window = int(num * 2 / 3)  # 2
            minimum_regularized_window = max(2, minimum_regularized_window)
        if regularize_or_insert_windows(minimum_regularized_window):
            logging.info('regularize windows')
        elif force_tiling:
            logging.info('force tiling')
            force_tile()
        else:
            return False

        # Make sure the current active window is raised to top of the stack.
        # The stack order will be used to find out previous active windows.
        active = windowlist.get_active_window()
        if active is not None:
            windowlist.raise_window(active)
    return True


def force_tile():

    winlist = windowlist.windowInCurrentWorkspaceInStackingOrder

    tile = workarea.tile(len(winlist))
    return windowlist.arrange(tile, winlist)


def resize(resize_width, resize_height):
    if resize_kdtree(resize_width, resize_height):
        return True
    return moveandresize([0, 0, resize_width, resize_height])


def move(target):
    if move_kdtree(target, allow_create_new_node=True):
        return True
    if move_kdtree(target, allow_create_new_node=False):
        return True
    target = {'left': [-config.MOVE_STEP, 0, 0, 0],
              'down': [0, config.MOVE_STEP, 0, 0],
              'up': [0, -config.MOVE_STEP, 0, 0],
              'right': [config.MOVE_STEP, 0, 0, 0], }[target]
    return moveandresize(target)


def moveandresize(target):
    active = windowlist.get_active_window(allow_outofworkspace=True)
    # cannot find target window
    if active is None:
        return False
    lay = windowlist.windowGeometry[active]
    for i in range(4):
        lay[i] += target[i]
    windowlist.arrange([lay], [active])
    return True


def swap(target):

    active = windowlist.get_active_window()

    if active is None:
        return False

    target_window_id = find_kdtree(active, target, allow_parent_sibling=False)

    if target_window_id is None:
        target_window_id = find(active, target)

    if target_window_id is None:
        target_window_id = find_kdtree(
            active, target, allow_parent_sibling=True)

    if target_window_id is None:
        return False

    lay0 = windowlist.windowGeometry[active]
    lay1 = windowlist.windowGeometry[target_window_id]

    windowlist.arrange([lay0, lay1], [target_window_id, active])
    return True


def find(center, target, allow_outofworkspace=False):
    '''
    find the nearest window in the target direction.
    '''

    def cal_center(x, y, w, h): return [x + w / 2.2, y + h / 2.2]
    if center is None:
        lay_center = workarea.width / 2.0, workarea.height / 2.0
    else:
        lay_center = windowlist.windowGeometry[center]
        lay_center = cal_center(*lay_center)
    _min = -1
    _r = None
    if allow_outofworkspace:
        winlist = windowlist.windowName
    else:
        winlist = windowlist.windowInCurrentWorkspaceInStackingOrder
    for w in winlist:
        l = windowlist.windowGeometry[w]
        l = cal_center(*l)
        bias1, bias2 = 1.0, 1.0
        bias = 4.0
        if target == 'down':
            delta = l[1] - lay_center[1]
            delta2 = (l[1] - lay_center[1]) ** 2 - (l[0] - lay_center[0]) ** 2
            bias1 = bias
        if target == 'up':
            delta = lay_center[1] - l[1]
            delta2 = (l[1] - lay_center[1]) ** 2 - (l[0] - lay_center[0]) ** 2
            bias1 = bias
        if target == 'right':
            delta = l[0] - lay_center[0]
            delta2 = (l[0] - lay_center[0]) ** 2 - (l[1] - lay_center[1]) ** 2
            bias2 = bias
        if target == 'left':
            delta = lay_center[0] - l[0]
            delta2 = (l[0] - lay_center[0]) ** 2 - (l[1] - lay_center[1]) ** 2
            bias2 = bias
        distance = bias1 * (l[0] - lay_center[0]) ** 2 + \
            bias2 * (l[1] - lay_center[1]) ** 2
        if delta > 0 and delta2 > 0:
            if _min == -1 or distance < _min:
                _min = distance
                _r = w
    return _r


def focus(target):

    active = windowlist.get_active_window(allow_outofworkspace=False)

    if active is not None:
        window_name = windowlist.windowName[active]
        if vim.navigate(window_name, target):
            return
        if emacs.navigate(window_name, target):
            return

    target_window_id = find_kdtree(active, target, allow_parent_sibling=False)

    if target_window_id is None:
        target_window_id = find(
            active, target,
            allow_outofworkspace=config.NavigateAcrossWorkspaces)

    if target_window_id is None:
        target_window_id = find_kdtree(
            active, target, allow_parent_sibling=True)

    if target_window_id is None:
        windowlist.raise_window(active)
    else:
        windowlist.raise_window(target_window_id)
    return True


def grow_width():
    resize(config.RESIZE_STEP, 0)


def grow_height():
    resize(0, config.RESIZE_STEP)


def shrink_width():
    resize(-config.RESIZE_STEP, 0)


def shrink_height():
    resize(0, -config.RESIZE_STEP)
