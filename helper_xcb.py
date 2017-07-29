import os
import xcffib
from xcffib.xproto import EventMask
from xcffib.testing import XvfbTest
from xcffib.xproto import GetPropertyType, Atom,ConfigWindow

conn = xcffib.connect(os.environ['DISPLAY'])
xproto = xcffib.xproto.xprotoExtension(conn)
screen = conn.get_setup().roots[conn.pref_screen]


def intern(name):
    return xproto.InternAtom(False, len(name), name).reply().atom


def getProperty(name, window=screen.root):
    return xproto.GetProperty(False, window, name,
                              xcffib.xproto.GetPropertyType.Any,
                              #     xcffib.xproto.Atom.WINDOW,
                              0, 2**32 - 1)


CLIENT_LIST = intern("_NET_CLIENT_LIST")
NET_WM_DESKTOP = intern("_NET_WM_DESKTOP")
NET_WM_NAME = intern("_NET_WM_NAME")
NET_FRAME_EXTENTS=intern("_NET_FRAME_EXTENTS")
NET_WM_STATE= intern("_NET_WM_STATE")
WM_STATE= intern("WM_STATE")

def arrange(layout, windowids):
    for lay,winid in zip(layout,windowids):
        xproto.ConfigureWindow(winid,
                ConfigWindow.X|ConfigWindow.Y|ConfigWindow.Width|ConfigWindow.Height,
                lay)
    conn.flush()

def get_window_list():
    for winid in getProperty(CLIENT_LIST).reply().value.to_atoms():
        yield (winid,
                getProperty(NET_WM_DESKTOP,winid),
                getProperty(NET_WM_NAME,winid),
                getProperty(Atom.WM_NAME,winid),
                getProperty(Atom.WM_CLASS,winid),
                getProperty(WM_STATE,winid),
                getProperty(NET_WM_STATE,winid),
                xproto.GetGeometry(winid),
                getProperty(NET_FRAME_EXTENTS,winid),)

def get_window_list_reply():
    lst=get_window_list()
    lst=list(lst)
    for winid,desktop,netwmname,wmname,wmclass,wmstate,netwmstate,geo,fextents in lst:
        yield (winid,
                desktop.reply().value.to_atoms()[0],
                netwmname.reply().value.to_string(),
                wmname.reply().value.to_string(),
                wmclass.reply().value.to_string().split('\x00')[:-1],
                wmstate.reply().value.to_atoms(),
                netwmstate.reply().value.to_atoms(),
                geo.reply().__dict__,
                fextents.reply().value.to_atoms(),)

if __name__ == '__main__':
    for w in get_window_list_reply():
        print(w)
