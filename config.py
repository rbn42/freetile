#!/usr/bin/python
WinBorder = 2
LeftPadding = 15
BottomPadding = 15
TopPadding = BottomPadding
RightPadding = BottomPadding
NavigateAcrossWorkspaces = True  # availabe in viewports desktops
TempFile = "/tmp/kd_tree_tile"
LockFile = "/tmp/kd_tree_tile_lock"
LogFile = ""  # '/tmp/kd_tree_tile.log'


# This is the congiguration that works for unity7. If you are using a
# different Desktop Environment, close all windows and execute "wmctrl
# -lG" to find out all the applications need to exclude.

EXCLUDE_APPLICATIONS = ['<unknown>', 'x-nautilus-desktop', 'unity-launcher',
                        'unity-panel', 'Hud', 'unity-dash', 'Desktop',
                        'Docky', 'conky', 'Conky'
                        'screenkey', 'XdndCollectionWindowImp']
# An alternative method to exclude applications.
EXCLUDE_WM_CLASS = ['conky', 'Conky', ]

UNRESIZABLE_APPLICATIONS = ['Screenkey']

RESIZE_STEP = 50
MOVE_STEP = 50
MIN_WINDOW_WIDTH = 50
MIN_WINDOW_HEIGHT = 50

# If you want work with 2x2 grids, which does not exist in i3-wm as I know.
ALLOW_2x2_GRID = False
ALLOW_3x3_GRID = False

MAX_KD_TREE_BRANCH = 0
if ALLOW_2x2_GRID:
    MAX_KD_TREE_BRANCH = 2
if ALLOW_3x3_GRID:
    MAX_KD_TREE_BRANCH = 3

# support compiz0.8
COMPIZ0_8 = False

# Allow the regularize algorithm to extend windows to full screen. Does not
# work very well in some desktop environments.
REGULARIZE_FULLSCREEN = False

# overwrite default configuration
import os.path
config_file = os.path.expanduser("~/.tilerc")
try:
    s = open(config_file).read()
    exec(s)
except:
    pass
