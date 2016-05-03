#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Window tiling for X

Usage:
  main.py layout (next|prev)
  main.py (focus|move|swap) (up|down|left|right)
  main.py (grow|shrink) (height|width)
  main.py cycle 
  main.py anticycle 
  main.py (save|load) <layout_id>
  main.py -h | --help

Options:
  -h --help     Show this screen.
"""
from locker import lock, unlock
import config
from util_tile import get_current_tile
from util import sort_win_list
from util_kdtree import find_kdtree, resize_kdtree, move_kdtree, insert_focused_window_into_kdtree,\
    regularize_windows
from util_wmctrl import arrange, move_window
from util_xdotool import get_active_window, raise_window
from config import LockFile


def change_tile_or_insert_new_window(shift):
    if len(WinList) < 1:
        return
    if shift < 0:
        change_tile(shift)
        return

    if len(WinList) == 1 + len(OldWinList):
        if insert_focused_window_into_kdtree():
            return
    if len(WinList) < len(OldWinList) or len(WinList) > len(OldWinList):
        print(1)
        print(WinList)
        print(OldWinList)
        if regularize_windows():
            PERSISTENT_DATA['winlist'] = WinList
            return
    if len(WinList) == len(OldWinList):
        change_tile(shift)
    else:
        change_tile(0)


def change_tile(shift):
    # TODO available tiling layouts
    from tiles import get_columns_tile2, get_horiz_tile, get_vertical_tile, get_fair_tile, get_autogrid_tile, maximize, minimize, get_simple_tile
    tiles_map = {
        'col2_l': lambda w: get_columns_tile2(w, reverse=False, cols=2),
        'col2_r': lambda w: get_columns_tile2(w, reverse=True, cols=2),
        'simple': get_simple_tile,
        'col1': lambda w: get_columns_tile2(w, reverse=False, cols=1),
        'horiz': get_horiz_tile,
        'vertical': get_vertical_tile,
        'fair': get_fair_tile,
        'autogrid': get_autogrid_tile,
        'maximize': maximize,
        'minimize': minimize,
    }

    winlist = sort_win_list(WinList, OldWinList)

    if len(winlist) < 2:
        TILES = []
    elif len(winlist) % 2 == 0:
        TILES = ['col2_l']
    else:
        TILES = ['col2_l', 'col2_r']
    if len(winlist) > 3:
        TILES.append('simple')
    if len(winlist) > 1:
        TILES.append('col1')
    TILES.append('maximize')

    # for rotated screen
    if MaxWidth < MaxHeight:
        if len(winlist) > 1:
            TILES = ['col1']
        TILES.append('maximize')

    # TODO unable to compare windows's numbers between different workspaces

    t = PERSISTENT_DATA.get('tile', None)
    arrange_twice = False
    NOFRAME_LAYOUTS = ['maximize', 'minimize']
    if t in NOFRAME_LAYOUTS:
        # arrange windows twice to get exact frame size
        arrange_twice = True

    if 0 == shift and t in tiles_map:
        pass
    elif t in TILES:
        i0 = TILES.index(t)
        i1 = i0 + shift
        t = TILES[i1 % len(TILES)]
    else:
        t = TILES[0]

    tile = tiles_map[t](len(winlist))
    if not None == tile:
        arrange(tile, winlist)
        if arrange_twice:
            arrange(tile, winlist)

    PERSISTENT_DATA['overall_position'] = None
    PERSISTENT_DATA['tile'] = t
    PERSISTENT_DATA['winlist'] = winlist


def cycle(reverse=False):
    winlist = sort_win_list(WinList, OldWinList)
    lay = get_current_tile(winlist, WinPosInfo)
    shift = -1 if reverse else 1
    winlist = winlist[shift:] + winlist[:shift]
    arrange(lay, winlist)

    active = get_active_window()
    i0 = winlist.index(active)
    i1 = (i0 + shift) % len(winlist)
    raise_window(winlist[i1])

    PERSISTENT_DATA['winlist'] = winlist


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
    active = get_active_window()
    # cannot find target window
    if None == active:
        return False
    lay = get_current_tile([active], WinPosInfo)[0]
    for i in range(4):
        lay[i] += target[i]
    arrange([lay], [active])
    #move_window(active, *lay)
    return True


def swap(target):

    winlist = sort_win_list(WinList, OldWinList)
    active = get_active_window()

    if None == active:
        return False

    target_window_id = find_kdtree(active, target, allow_parent_sibling=False)

    if None == target_window_id:
        target_window_id = find(active, target, winlist, WinPosInfo)

    if None == target_window_id:
        target_window_id = find_kdtree(
            active, target, allow_parent_sibling=True)

    if None == target_window_id:
        return False

    i0 = winlist.index(active)
    i1 = winlist.index(target_window_id)

    lay = get_current_tile(winlist, WinPosInfo)
    print(lay)
    arrange([lay[i0], lay[i1]], [winlist[i1], winlist[i0]])

    winlist[i0], winlist[i1] = winlist[i1], winlist[i0]
    PERSISTENT_DATA['winlist'] = winlist
    return True


def find(center, target, winlist, posinfo):
    '''
    find the nearest window in the target direction.
    '''
    lay = get_current_tile(winlist, posinfo)
    cal_center = lambda x, y, w, h: [x + w / 2.2, y + h / 2.2]
    if None == center:
        lay_center = MaxWidth / 2.0, MaxHeight / 2.0
    else:
        lay_center = get_current_tile([center], WinPosInfo)[0]
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


def focus(target):

    active = get_active_window(allow_outofworkspace=True)

    target_window_id = find_kdtree(active, target, allow_parent_sibling=False)

    if None == target_window_id:
        if config.NavigateAcrossWorkspaces:
            Windows = WinListAll
        else:
            Windows = WinList
        target_window_id = find(active, target, Windows, WinPosInfo)

    if None == target_window_id:
        target_window_id = find_kdtree(
            active, target, allow_parent_sibling=True)

    if None == target_window_id:
        raise_window(active)
    else:
        raise_window(target_window_id)
    return True


def store():
    active = get_active_window()
    if not None == active:
        h = PERSISTENT_DATA.get('active_history', [])
        h.insert(0, active)
        PERSISTENT_DATA['active_history'] = h[:1000]
    with open(config.TempFile, 'w') as f:
        PERSISTENT_DATA_ALL[Desktop] = PERSISTENT_DATA
        f.write(str(PERSISTENT_DATA_ALL))

from global_variables import PERSISTENT_DATA, PERSISTENT_DATA_ALL, WinList, WinPosInfo, WinListAll, MaxHeight, MaxWidth
from global_variables import Desktop, OldWinList

if __name__ == '__main__':
    if lock(LockFile):
        from docopt import docopt
        arguments = docopt(__doc__)

        for target in ('up', 'down', 'left', 'right'):
            if arguments[target]:
                break

        if False:
            pass
        elif arguments['cycle']:
            cycle()
        elif arguments['anticycle']:
            cycle(reverse=True)
        elif arguments['swap']:
            swap(target)
        elif arguments['move']:
            move(target)
        elif arguments['focus']:
            focus(target)

        elif arguments['layout']:
            assert not arguments['next'] == arguments['prev']
            change_tile_or_insert_new_window(
                shift=-1 if arguments['prev'] else 1)
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

        store()

        unlock(LockFile)
