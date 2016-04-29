from execute import execute_and_output
import re


def get_wm_class(winid):
    s = execute_and_output('xprop -id %s | grep WM_CLASS' % winid)
    s = re.findall('^.+?\=(.+)', s)[0]
    return eval(s)


def get_window_frame_size(winid):
    try:
        s = execute_and_output(
            'xprop -id %s | grep _NET_FRAME_EXTENTS' % winid)
        l = re.findall('\d+', s)
        return [int(i) for i in l]
    except:
        return 0, 0, 0, 0