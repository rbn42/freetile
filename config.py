#!/usr/bin/python
WinBorder = 2
LeftPadding = 4
BottomPadding = 4
TopPadding = 4
RightPadding = 4
NavigateAcrossWorkspaces = False  # True  # availabe in viewports desktops

EXCLUDE_APPLICATIONS = ['<unknown>', 'x-nautilus-desktop', 'unity-launcher',
                        'unity-panel', 'Hud', 'unity-dash', 'Desktop',
                        'Docky', 'conky', 'Conky'
                        'screenkey', 'XdndCollectionWindowImp']
EXCLUDE_WM_CLASS = ['conky', 'Conky', ]

RESIZE_STEP = 72
MOVE_STEP = 72
MIN_WINDOW_WIDTH = 50
MIN_WINDOW_HEIGHT = 50

MAX_KD_TREE_BRANCH = 3

REGULARIZE_FULLSCREEN = True

# find out vim server name in window title, and send vim navigation command.
VIM_SERVER_NAME = " - (VIMSERVER\d+)$"
VIM_NAVIGATION_CMD = """vim --servername {vimserver} --remote-expr "TileFocusWindow('{target}')" """
VIM_SERVER_NAME = None

EMACS_WINDOW_NAME = ".+emacs.+"
EMACS_NAVIGATION_CMD = "emacsclient -e '(evil-window-{target} 1)'"
EMACS_WINDOW_NAME = None

# overwrite default configuration
import os.path

config_file = os.path.expanduser("~/.tilerc")
try:
    s = open(config_file).read()
    exec(s)
except:
    pass
