import os

import xcffib
from xcffib.testing import XvfbTest
from xcffib.xproto import Atom, ConfigWindow, EventMask, GetPropertyType

conn = xcffib.connect(os.environ['DISPLAY'])
xproto = xcffib.xproto.xprotoExtension(conn)


def arrange(layout, windowids):
    for lay, winid in zip(layout, windowids):
        xproto.ConfigureWindow(winid,
                               ConfigWindow.X | ConfigWindow.Y
                               | ConfigWindow.Width | ConfigWindow.Height,
                               lay)
    conn.flush()


def move(winid, x, y, sync=True):
    xproto.ConfigureWindow(winid,
                           ConfigWindow.X | ConfigWindow.Y,
                           [x, y])
    if sync:
        conn.flush()
