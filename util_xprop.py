from execute import execute_and_output
import re


def get_wm_class(winid):
    cmd = 'xprop -id %s | grep WM_CLASS'
    cmd = 'xprop -id %s WM_CLASS'
    s = execute_and_output(cmd % winid)
    s = re.findall('^.+?\=(.+)', s)[0]
    return eval(s)


def get_window_frame_size(winid):
    try:
        cmd = 'xprop -id %s | grep _NET_FRAME_EXTENTS'
        cmd = 'xprop -id %s _NET_FRAME_EXTENTS'
        s = execute_and_output(cmd % winid)
        l = re.findall('\d+', s)
        if len(l) < 4:
            return 0, 0, 0, 0
        return [int(i) for i in l]
    except:
        return 0, 0, 0, 0


def get_window_state(winid):
    try:
        cmd = 'xprop -id %s | grep state '
        cmd = 'xprop -id %s  WM_STATE'
        s = execute_and_output(cmd % winid)
    except:
        return False
    if 'window state: Normal' in s:
        return True
    return False


def get_wm_class_and_state(winid):
    cmd = 'xprop -id %s | grep WM_CLASS'
    cmd = 'xprop -id %s WM_CLASS WM_STATE'
    s = execute_and_output(cmd % winid)
    wm_class = re.findall('^.+?\=(.+)', s)[0]
    minimized = 'window state: Normal' not in s
    return eval(wm_class), minimized
