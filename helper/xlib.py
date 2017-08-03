import Xlib
from Xlib import X, display, protocol

disp = display.Display()
screen = disp.screen()
root = screen.root
# sync lock
# TODO
# disp.sync()


def edit_prop(window, mode, name, value):
    cm_event = protocol.event.ClientMessage(
        window=window,
        client_type=disp.intern_atom(name),
        data=(32, [mode, disp.intern_atom(value), 0, 0, 0])
    )
    disp.send_event(root, cm_event,
                    (X.SubstructureRedirectMask | X.SubstructureNotifyMask))


def get_root_window_property(name):
    return root.get_property(disp.intern_atom(name),
                             Xlib.Xatom.CARDINAL, 0, 32).value


def get_window(func):
    def func_wrapper(win):
        t = type(win)
        if t == int:
            win = disp.create_resource_object('window', win)
            r = func(win)
        elif t == type(root):
            r = func(win)
        elif "Xlib.display.Window" in str(win):
            r = func(win)
        else:
            print(str(win))
        return r
    return func_wrapper


def get_frame_extents(win):
    frame_extents = win.get_property(disp.intern_atom(
        "_NET_FRAME_EXTENTS"), Xlib.Xatom.CARDINAL, 0, 32)
    if frame_extents is None:
        return 0, 0, 0, 0
    else:
        return frame_extents.value


@get_window
def get_wm_class_and_state(win):
    wm_class = win.get_wm_class()
    wm_state = win.get_wm_state()
    minimized = not wm_state.state == 1
    return wm_class, minimized
