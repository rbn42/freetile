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
import re


def maximize_one(windowid, sync=True):
    command = " wmctrl -i -r %d -badd,maximized_vert,maximized_horz" % windowid
    if not sync:
        command += ' &'
    execute(command)


def get_windowmanager():
    cmd = 'wmctrl -m'
    out = execute_and_output(cmd)
    _class = re.findall('Class:(.+)', out)[0]
    _name = re.findall('Name:(.+)', out)[0]
    return _name.strip(), _class.strip()
