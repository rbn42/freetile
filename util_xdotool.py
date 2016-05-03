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

from execute import execute_and_output, execute

from global_variables import WinList, WinPosInfo
import re


def get_active_window_xprop(allow_outofworkspace=False):
    cmd = "xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW"
    s = execute_and_output(cmd)
    active = re.findall('_NET_ACTIVE_WINDOW\(WINDOW\)(.+)', s)
    if len(active) < 1:
        return None
    active = int(active[0], 16)
    if active not in WinPosInfo:
        return None
    if allow_outofworkspace:
        return active
    if active not in WinList:
        return None
    return active


def get_active_window(allow_outofworkspace=False):
    return get_active_window_xprop(allow_outofworkspace)

    active = int(execute_and_output("xdotool getactivewindow").split()[0])
    if active not in WinPosInfo:
        return None
    if allow_outofworkspace:
        return active
    if active not in WinList:
        return None
    assert active == get_active_window_xprop(allow_outofworkspace)
    return active


def minimize_one(windowid):
    command = 'xdotool windowminimize %d' % windowid
    execute(command)


def raise_window(windowid):
    if False:
        command = 'xdotool windowactivate %d' % windowid
    command = "wmctrl -i -a %d" % windowid
    execute(command)
