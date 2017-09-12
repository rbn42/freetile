#!/usr/bin/python
window_gap = 4
left_padding = 4
bottom_padding = 4
top_padding = 4
right_padding = 4
navigate_across_workspaces = False  # True  # availabe in viewports desktops

exclude_wm_name = []
exclude_wm_class = []

resize_step = 72
move_step = 72
min_window_width = 50
min_window_height = 50

max_tree_branch = 3

fullscreen_tiling = True
maximize_single_window = True


# overwrite default configuration
import os.path

config_file = os.path.expanduser("~/.config/freetilerc")
try:
    s = open(config_file).read()
    exec(s)
except BaseException:
    pass
