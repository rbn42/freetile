"""
Operations for overlapped layout.
"""
from .windowlist import windowlist
from .workarea import workarea
from . import config


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


def move(target):
    target = {'left': [-config.move_step, 0, 0, 0],
              'down': [0, config.move_step, 0, 0],
              'up': [0, -config.move_step, 0, 0],
              'right': [config.move_step, 0, 0, 0], }[target]
    return moveandresize(target)


def cal_center(x, y, w, h): return [x + w / 2.2, y + h / 2.2]


def find(center, target, allow_outofworkspace=False):
    '''
    find the nearest window in the target direction.
    '''

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
