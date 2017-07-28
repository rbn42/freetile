from helper_xlib import get_frame_extents


def get_current_tile(wins, posinfo):
    l = []
    for _id in wins:
        _name, _pos = posinfo[_id]
        x, y, w, h = _pos
        f_left, f_right, f_top, f_bottom = get_frame_extents(_id)
        y -= f_top
        x -= f_left
        h += f_top + f_bottom
        w += f_left + f_right

        l.append([x, y, w, h])
    return l
