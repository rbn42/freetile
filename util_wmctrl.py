############################################################################
# Copyright (c) 2009   unohu <unohu0@gmail.com>                            #
#                                                                          #
# Permission to use, copy, modify, and/or distribute this software for any #
# purpose with or without fee is hereby granted, provided that the above   #
# copyright notice and this permission notice appear in all copies.        #
#                                                                          #
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES #
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF         #
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR  #
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES   #
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN    #
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF  #
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.           #
#                                                                          #
############################################################################

from util_xprop import get_window_frame_size
from execute import execute_and_output, execute


def move_window(windowid, x, y, w, h, sync=True):
    # Unmaximize window

    f_left, f_right, f_top, f_bottom = get_window_frame_size(windowid)
    w -= f_left + f_right
    h -= f_top + f_bottom

    #wmclass = get_wm_class(windowid)
    # for n in config.NOFRAME_WMCLASS:
    #    if n in wmclass:
    #        break
    try:
        if 'Stati' in execute_and_output('xprop -id %s WM_NORMAL_HINTS| grep gravi' % windowid):
            y += f_top
            x += f_left
    except:
        pass
    # Now move it
    command = "wmctrl -i -r %d -e 0,%d,%d,%d,%d" % (windowid, x, y, w, h)
    if not sync:
        command += ' &'
    return command
    execute(command)

    #command = 'xdotool windowmove  %d %d %d' % (windowid, x, y)
    # execute(command)
    #command = 'xdotool windowsize  %d %d %d' % (windowid, w, h)
    # execute(command)
    #command = "wmctrl -i -r " + windowid + " -b remove,hidden,shaded"
#    command = 'xdotool windowmap "%s"' % windowid
#    command = 'xdotool windowactivate "%s"' % windowid


def unmaximize_one(windowid, sync=True):
    command = " wmctrl -i -r %d -bremove,maximized_vert,maximized_horz" % windowid
    if not sync:
        command += ' &'
    execute(command)


def maximize_one(windowid, sync=True):
    command = " wmctrl -i -r %d -badd,maximized_vert,maximized_horz" % windowid
    if not sync:
        command += ' &'
    execute(command)


def arrange(layout, windows):
    cmds = []
    for win, lay in zip(windows, layout):
        cmd = move_window(win, *lay, sync=False)
        cmds.append(cmd)
    for win in windows:
        unmaximize_one(win, sync=False)
    for cmd in cmds:
        execute(cmd)
