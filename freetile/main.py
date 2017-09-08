from . import config
from . import nontree
import logging

from .util_kdtree import (find_kdtree, move_kdtree,
                          regularize_or_insert_windows, resize_kdtree)
from .windowlist import windowlist
from .workarea import workarea


def regularize(
        ignore_overlapped_layout=False,
        minimum_regularized_window=None):
    '''
    Try to regularize windows or add a new window into the K-D tree.
    '''
    logging.info('regularize layout')
    stack = windowlist.windowInCurrentWorkspaceInStackingOrder
    num = len(stack)
    if num == 0:
        pass
    elif num == 1 and config.maximize_single_window:
        windowlist.maximize_window(stack[0])
    else:
        """
        Allow to insert 1/3 new windows to a regularized layout of the rest 2/3 windows.
        """
        if minimum_regularized_window is None:
            minimum_regularized_window = max(min(num - 1, 2), num * 2 // 3, 1)

        if regularize_or_insert_windows(minimum_regularized_window):
            logging.info('regularize windows')
        elif not ignore_overlapped_layout:
            logging.info('force tiling')
            force_tiling()
        else:
            return False

        # Make sure the current active window is raised to top of the stack.
        # The stack order will be used to find out previous active windows.
        active = windowlist.get_active_window()
        if active is not None:
            windowlist.raise_window(active)

    return True


def force_tiling():
    winlist = windowlist.windowInCurrentWorkspaceInStackingOrder
    tile = workarea.tile(len(winlist))
    return windowlist.arrange(tile, winlist)


def resize(resize_width, resize_height):
    return resize_kdtree(resize_width, resize_height) \
        or nontree.moveandresize([0, 0, resize_width, resize_height])


def move(target):
    return move_kdtree(target, allow_create_new_node=True) \
        or move_kdtree(target, allow_create_new_node=False) \
        or nontree.move(target)


def swap(target):

    active = windowlist.get_active_window()

    if active is None:
        return False

    target_window_id = find_kdtree(active, target, False) \
        or nontree.find(active, target) \
        or find_kdtree(active, target, True)

    if target_window_id is None:
        return False

    lay0 = windowlist.windowGeometry[active]
    lay1 = windowlist.windowGeometry[target_window_id]

    windowlist.arrange([lay0, lay1], [target_window_id, active])
    return True


def focus(target):

    active = windowlist.get_active_window(allow_outofworkspace=False)

    target_window_id = find_kdtree(active, target, False) \
        or nontree.find(active, target, config.navigate_across_workspaces) \
        or find_kdtree(active, target, True)

    if target_window_id is None:
        windowlist.raise_window(active)
    else:
        windowlist.raise_window(target_window_id)
    return True


def grow_width():
    resize(config.resize_step, 0)


def grow_height():
    resize(0, config.resize_step)


def shrink_width():
    resize(-config.resize_step, 0)


def shrink_height():
    resize(0, -config.resize_step)
