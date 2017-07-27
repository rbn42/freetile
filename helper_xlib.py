from Xlib import X, display, Xutil, protocol
disp = display.Display()
#winid = window.winId()

def arrange(layout, windows):
    for winid,lay in zip(windows,layout):
        x,y,width,height=lay
        window_xlib = disp.create_resource_object('window', winid)
        window_xlib.configure(x=x, y=y, width=width, height=height)
    disp.flush()
