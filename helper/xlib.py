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


@get_window
def maximize(win):
    edit_prop(win, 1, '_NET_WM_STATE', '_NET_WM_STATE_MAXIMIZED_VERT')
    edit_prop(win, 1, '_NET_WM_STATE', '_NET_WM_STATE_MAXIMIZED_HORZ')
    disp.flush()


@get_window
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


def arrange(layout, windowids):
    windows = [disp.create_resource_object('window', i)for i in windowids]
    # unmaximize
    for window_xlib in windows:
        edit_prop(window_xlib, 0, '_NET_WM_STATE',
                  '_NET_WM_STATE_MAXIMIZED_VERT')
        edit_prop(window_xlib, 0, '_NET_WM_STATE',
                  '_NET_WM_STATE_MAXIMIZED_HORZ')

    # TODO need correct frame extents data after maximized windows unmaximized
    # disp.flush()
    # disp.sync()
    import time
    time.sleep(0.1)

    windows_normal_hints = [w.get_wm_normal_hints() for w in windows]
    windows_frame_extents = [get_frame_extents(w) for w in windows]

    layout_final = []
    # move windows
    for windowid, window_xlib, lay, normal_hints, frame_extents in zip(
            windowids, windows, layout,
            windows_normal_hints, windows_frame_extents):
        x, y, width, height = lay
        f_left, f_right, f_top, f_bottom = frame_extents
        width -= f_left + f_right
        height -= f_top + f_bottom

        # window gravity: Static
        if normal_hints.win_gravity == 10:
            y += f_top
            x += f_left
        layout_final.append([x, y, width, height])
#        window_xlib.configure(x=x, y=y, width=width, height=height)
    import helper.xcb
    return helper.xcb.arrange(layout_final, windowids)
    # disp.flush()
