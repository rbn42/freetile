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


import os.path
from initialize import initialize_windows, initialize_desktop
from config import BottomPadding, RightPadding, LeftPadding, TopPadding,\
    TempFile

desktop, desktop_x, desktop_y, OrigXstr, OrigYstr, MaxWidthStr, MaxHeightStr = initialize_desktop()
WinList, WinListAll, WinPosInfo = initialize_windows(desktop)
Desktop = '%s,%s,%s' % (desktop, desktop_x, desktop_y)

MaxWidth = int(MaxWidthStr) - LeftPadding - RightPadding
MaxHeight = int(MaxHeightStr) - TopPadding - BottomPadding
OrigX = int(OrigXstr) + LeftPadding
OrigY = int(OrigYstr) + TopPadding

if os.path.exists(TempFile):
    PERSISTENT_DATA_ALL = eval(open(TempFile).read())
else:
    PERSISTENT_DATA_ALL = {}
PERSISTENT_DATA = PERSISTENT_DATA_ALL.get(Desktop, {})
OldWinList = PERSISTENT_DATA.get('winlist', [])
