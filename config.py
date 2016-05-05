WinBorder = 2
LeftPadding = 15
BottomPadding = 15
TopPadding = BottomPadding
RightPadding = BottomPadding
NavigateAcrossWorkspaces = True  # availabe in Unity7
TempFile = "/dev/shm/.ktt"
LockFile = "/dev/shm/.ktt_lock"


# This is the congiguration that works for unity7. If you are using a
# different Desktop Environment, close all windows and execute "wmctrl
# -lG" to find out all the applications need to exclude.

EXCLUDE_APPLICATIONS = ['<unknown>', 'x-nautilus-desktop', 'unity-launcher',
                        'unity-panel', 'Hud', 'unity-dash', 'Desktop',
                        'Docky',
                        'screenkey', 'XdndCollectionWindowImp']
# An alternative method to exclude applications.
EXCLUDE_WM_CLASS = ['wesnoth-1.12', 'vlc']

UNRESIZABLE_APPLICATIONS = ['Screenkey']
RESIZE_STEP = 50
MOVE_STEP = 50
MIN_WINDOW_WIDTH = 50
MIN_WINDOW_HEIGHT = 50

# NOFRAME_WMCLASS = ['Wine']

# In i3-wm's window tree, only one child of a node is allowed to split.
# MAX_KD_TREE_BRANCH = 1
MAX_KD_TREE_BRANCH = 2
