from Xlib import X, display, Xutil, protocol
import Xlib

disp = display.Display()
screen = disp.screen()
# sync lock
# TODO
# disp.sync()


def edit_prop(window, mode, name, value):
    cm_event = protocol.event.ClientMessage(
        window=window,
        client_type=disp.intern_atom(name),
        data=(32, [mode, disp.intern_atom(value), 0, 0, 0])
    )
    disp.send_event(screen.root, cm_event,
                    (X.SubstructureRedirectMask | X.SubstructureNotifyMask))


def arrange(layout, windowids):
    windows = []
    for windowid in windowids:
        window_xlib = disp.create_resource_object('window', windowid)
        windows.append(window_xlib)
    # unmaximize
    for window_xlib in windows:
        edit_prop(window_xlib, 0, '_NET_WM_STATE',
                  '_NET_WM_STATE_MAXIMIZED_VERT')
        edit_prop(window_xlib, 0, '_NET_WM_STATE',
                  '_NET_WM_STATE_MAXIMIZED_HORZ')

    # TODO need true frame extents data after maximized windows unmaximized
    #disp.flush()
    #disp.sync()
    import time
    time.sleep(0.1)

    window_normal_hints = []
    for window_xlib in windows:
        wm_normal_hints = window_xlib.get_wm_normal_hints()
        window_normal_hints.append(wm_normal_hints)

    # move windows
    for windowid, window_xlib, lay, wm_normal_hints in zip(windowids, windows, layout, window_normal_hints):
        x, y, width, height = lay
        frame_extents = window_xlib.get_property(disp.intern_atom(
            "_NET_FRAME_EXTENTS"), Xlib.Xatom.CARDINAL, 0, 32)
        if None == frame_extents:
            f_left, f_right, f_top, f_bottom = 0, 0, 0, 0
        else:
            f_left, f_right, f_top, f_bottom = frame_extents.value
        width -= f_left + f_right
        height -= f_top + f_bottom
    # TODO
#        print(wm_normal_hints)
#    if 'Stati' in str(wm_normal_hints):
#        y += f_top
#        x += f_left
        window_xlib.configure(x=x, y=y, width=width, height=height)
    disp.flush()
