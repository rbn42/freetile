#!/usr/bin/python
WindowGap = 4
LeftPadding = 4
BottomPadding = 4
TopPadding = 4
RightPadding = 4
NavigateAcrossWorkspaces = False  # True  # availabe in viewports desktops

EXCLUDE_APPLICATIONS = []
EXCLUDE_WM_CLASS = []

RESIZE_STEP = 72
MOVE_STEP = 72
MIN_WINDOW_WIDTH = 50
MIN_WINDOW_HEIGHT = 50

MAX_KD_TREE_BRANCH = 3

REGULARIZE_FULLSCREEN = True


# overwrite default configuration
import os.path

config_file = os.path.expanduser("~/.config/freetilerc")
try:
    s = open(config_file).read()
    exec(s)
except BaseException:
    pass
