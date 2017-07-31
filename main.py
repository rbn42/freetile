#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Window tiling for X

Usage:
  main.py regularize
  main.py (focus|move|swap) (up|down|left|right)
  main.py (grow|shrink) (height|width)
  main.py (save|load) <layout_id>
  main.py list
  main.py -h | --help

Options:
  -h --help     Show this screen.
"""
import config
import logging
import re
import subprocess

from helper_ewmh import raise_window
from helper_xlib import arrange, maximize
from util_kdtree import (find_kdtree, insert_focused_window_into_kdtree,
                         move_kdtree, regularize_windows, resize_kdtree)
from windowlist import windowlist
from workarea import workarea


def regularize():
    '''
    Try to regularize windows or add a new window into the K-D tree.
    '''
    if len(windowlist.windowInCurrentWorkspaceInStackingOrder) < 1:
        return True
    elif len(windowlist.windowInCurrentWorkspaceInStackingOrder) < 2:
        maximize(windowlist.windowInCurrentWorkspaceInStackingOrder[0])
        return True
    elif regularize_windows():
        logging.info('regularize windows')
        return True
    elif insert_focused_window_into_kdtree():
        logging.info('insert a window into the K-D Tree')
        return True
    else:
        logging.info('layout')
        return force_tile()


def force_tile():

    winlist = windowlist.windowInCurrentWorkspaceInStackingOrder

    tile = workarea.tile(len(winlist))
    return arrange(tile, winlist)


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
    lay = windowlist.get_current_layout()[0]
    for i in range(4):
        lay[i] += target[i]
    arrange([lay], [active])
    return True


def swap(target):

    winlist = windowlist.windowInCurrentWorkspaceInStackingOrder
    active = windowlist.get_active_window()

    if active is None:
        return False

    target_window_id = find_kdtree(active, target, allow_parent_sibling=False)

    if target_window_id is None:
        target_window_id = find(active, target, winlist, windowlist.windowInfo)

    if target_window_id is None:
        target_window_id = find_kdtree(
            active, target, allow_parent_sibling=True)

    if target_window_id is None:
        return False

    i0 = winlist.index(active)
    i1 = winlist.index(target_window_id)

    lay = windowlist.get_current_layout()
    arrange([lay[i0], lay[i1]], [winlist[i1], winlist[i0]])

    winlist[i0], winlist[i1] = winlist[i1], winlist[i0]
    return True


def find(center, target, winlist, posinfo):
    '''
    find the nearest window in the target direction.
    '''
    lay = windowlist.get_current_layout()

    def cal_center(x, y, w, h): return [x + w / 2.2, y + h / 2.2]
    if None == center:
        lay_center = workarea.width / 2.0, workarea.height / 2.0
    else:
        lay_center = windowlist.get_current_layout()[0]
        lay_center = cal_center(*lay_center)
    _min = -1
    _r = None
    for w, l in zip(winlist, lay):
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


def list_windows():
    print('current workspace')
    for w in windowlist.windowInCurrentWorkspaceInStackingOrder:
        print('%s,%s' % (w, windowlist.windowInfo[w]))
    print('all windows')
    for w in windowlist.windowInfo:
        print('%s,%s' % (w, windowlist.windowInfo[w]))


def focus(target):

    active = windowlist.get_active_window(allow_outofworkspace=False)

    if not None == config.VIM_SERVER_NAME:
        if not None == active:
            vimserver = re.findall(
                config.VIM_SERVER_NAME, windowlist.windowInfo[active][0])
            if len(vimserver) > 0:
                vimserver = vimserver[0]
                cmd = config.VIM_NAVIGATION_CMD.format(vimserver=vimserver,
                                                       target=target)
                s = subprocess.check_output(cmd, shell=True).decode('utf8')
                s = int(s)
                if s == 1:
                    return

    target_window_id = find_kdtree(active, target, allow_parent_sibling=False)

    if None == target_window_id:
        if config.NavigateAcrossWorkspaces:
            Windows = windowlist.windowInfo.keys()
        else:
            Windows = windowlist.windowInCurrentWorkspaceInStackingOrder
        target_window_id = find(active, target, Windows, windowlist.windowInfo)

    if None == target_window_id:
        target_window_id = find_kdtree(
            active, target, allow_parent_sibling=True)

    if None == target_window_id:
        raise_window(active)
    else:
        raise_window(target_window_id)
    return True


if __name__ == '__main__':
    windowlist.reset()
    from docopt import docopt
    arguments = docopt(__doc__)

    for target in ('up', 'down', 'left', 'right'):
        if arguments[target]:
            break

    if arguments['swap']:
        swap(target)
    elif arguments['move']:
        move(target)
    elif arguments['focus']:
        focus(target)
    elif arguments['regularize']:
        logging.info('regularize layout')
        regularize()
    elif arguments['grow']:
        if arguments['width']:
            resize(config.RESIZE_STEP, 0)
        else:
            resize(0, config.RESIZE_STEP)
    elif arguments['shrink']:
        if arguments['width']:
            resize(-config.RESIZE_STEP, 0)
        else:
            resize(0, -config.RESIZE_STEP)

    elif arguments['save']:
        print('not implemented')
    elif arguments['load']:
        print('not implemented')
    # debug
    elif arguments['list']:
        list_windows()

