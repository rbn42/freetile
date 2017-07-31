import logging
from config import (MAX_KD_TREE_BRANCH, MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH,
                    REGULARIZE_FULLSCREEN, WinBorder)

from helper_xlib import arrange
from tree import (build_tree, create_parent, create_sibling, getLayoutAndKey,
                  regularize, remove_single_child_node)
from windowlist import windowlist
from workarea import workarea


def resize_kdtree(resize_width, resize_height):
    '''
    Adjust non-overlapping layout.
    '''

    winlist = windowlist.windowInCurrentWorkspaceInStackingOrder
    # ignore layouts with less than 2 windows
    if len(winlist) < 2:
        return False

    active = windowlist.get_active_window()
    # can find target window
    if active is None:
        return False

    lay = windowlist.get_current_layout()
    # generate k-d tree
    _tree, _map = getkdtree(winlist, lay)
    current_node = _map[active]

    # determine the size of current node and parent node.
    if len(current_node.path) % 2 == 0:
        resize_current = resize_height
        resize_parent = resize_width
        index_current = 3
        index_parent = 2
    else:
        resize_current = resize_width
        resize_parent = resize_height
        index_current = 2
        index_parent = 3

    regularize_node = None

    # resize nodes
    if not resize_current == 0:
        if not current_node.overlap:
            if current_node.parent is not None:
                node = current_node
                index = index_current
                _resize = resize_current
                node.modified = True
                regularize_node = node.parent
                # invert the operation if the node is the last child of its
                # parent
                if regularize_node.children[-1] == node:
                    node.position[index] -= _resize
                else:
                    node.position[index] += _resize

    if not resize_parent == 0:
        if current_node.parent is not None:
            if not current_node.parent.overlap:
                if current_node.parent.parent is not None:
                    node = current_node.parent
                    index = index_parent
                    _resize = resize_parent
                    node.modified = True
                    regularize_node = node.parent
                    # invert the operation if the node is the last child of its
                    # parent
                    if regularize_node.children[-1] == node:
                        node.position[index] -= _resize
                    else:
                        node.position[index] += _resize

    if regularize_node is None:
        return False
    regularize_node = regularize_node.parent

    if REGULARIZE_FULLSCREEN:
        _tree.position = [workarea.x, workarea.y, workarea.x +
                          workarea.width, workarea.y + workarea.height]
        return regularize_kd_tree(_tree)
    return regularize_kd_tree(regularize_node)


def getkdtree(winlist, lay):
    origin_lay = [[x, y, x + w, y + h] for x, y, w, h in lay]
    _tree, _map = build_tree(zip(origin_lay, winlist))
    return _tree, _map


def insert_window_into_kdtree(winid, target):
    winlist = [
        w for w in windowlist.windowInCurrentWorkspaceInStackingOrder
        if not w == winid]
    lay = windowlist.get_current_layout()
    _tree, _map = getkdtree(winlist, lay)
    target_node = _map[target]
    if target_node.parent.overlap:
        return False
    node = create_sibling(target_node)
    node.key = winid
    node.leaf = True
    if REGULARIZE_FULLSCREEN:
        _tree.position = [workarea.x, workarea.y, workarea.x +
                          workarea.width, workarea.y + workarea.height]
        return regularize_kd_tree(_tree)
    return regularize_kd_tree(node.parent)


def move_kdtree(target, allow_create_new_node=True):
    '''
    Adjust non-overlapping layout.
    '''

    active = windowlist.get_active_window()
    # can find target window
    if active is None:
        return False

    # sort_win_list(windowlist.windowInCurrentWorkspaceInStackingOrder)
    winlist = windowlist.windowInCurrentWorkspaceInStackingOrder
    # ignore layouts with less than 2 windows
    if len(winlist) < 2:
        return False

    lay = windowlist.get_current_layout()
    # generate k-d tree
    _tree, _map = getkdtree(winlist, lay)
    current_node = _map[active]

    # whether promote node to its parent's level
    if len(current_node.path) % 2 == 0:
        promote = target in ['right', 'left']
    else:
        promote = target in ['down', 'up']
    shift = 0 if target in ['left', 'up'] else 1

    if promote:
        current_node.parent.children.remove(current_node)
        regularize_node = current_node.parent.parent
        index_parent = regularize_node.children.index(current_node.parent)
        regularize_node.children.insert(index_parent + shift, current_node)
    else:
        regularize_node = current_node.parent
        index_current = regularize_node.children.index(current_node)
        regularize_node.children.remove(current_node)
        '''
        If there is no more nodes at the target direction, promote the current node.
        '''
        if 0 <= index_current - 1 + shift < len(regularize_node.children):

            # If there are is only one sibling node, promote them both.
            if len(regularize_node.children) == 1:
                #
                shift = -1 if target in ['left', 'up'] else 1
                regularize_node.children.insert(
                    index_current + shift, current_node)
            else:
                new_parent = regularize_node.children[
                    index_current - 1 + shift]
                # If there is a leaf node at the target direction, build a new
                # parent node for the leaf node and the current node.
                _swap = False or not allow_create_new_node
                if new_parent.leaf and not _swap:
                    # But allow no more than one branch for each node
                    non_leaf_node_count = 0
                    for sibling in new_parent.parent.children:
                        if not sibling.leaf or MAX_KD_TREE_BRANCH < 1:
                            non_leaf_node_count += 1
                            if not non_leaf_node_count < MAX_KD_TREE_BRANCH:
                                # Just swap them.
                                _swap = True
                                break
                    else:
                        new_parent = create_parent(new_parent)
                if _swap:
                    shift = -1 if target in ['left', 'up'] else 1
                    regularize_node.children.insert(
                        index_current + shift, current_node)
                else:
                    new_parent.children.append(current_node)
        else:
            # promote the current node.
            regularize_node = current_node.parent.parent.parent
            index_current = regularize_node.children.index(
                current_node.parent.parent)
            regularize_node.children.insert(
                index_current + shift, current_node)

        if len(regularize_node.children) == 1:
            regularize_node = regularize_node.parent

    # remove nodes which has only one child
    remove_single_child_node(regularize_node)

    if regularize_node.overlap:
        return False

    # regularize k-d tree
    regularize_node = regularize_node.parent
    if REGULARIZE_FULLSCREEN:
        _tree.position = [workarea.x, workarea.y, workarea.x +
                          workarea.width, workarea.y + workarea.height]
        return regularize_kd_tree(_tree)
    return regularize_kd_tree(regularize_node, min_width=1, min_height=1)


def regularize_windows():
    lay = windowlist.get_current_layout()
    _tree, _map = getkdtree(
        windowlist.windowInCurrentWorkspaceInStackingOrder, lay)
    if _tree.overlap:
        logging.info('overlapped windows')
        return False
    if REGULARIZE_FULLSCREEN:
        _tree.position = [workarea.x, workarea.y, workarea.x +
                          workarea.width, workarea.y + workarea.height]
    return regularize_kd_tree(_tree)


def regularize_kd_tree(regularize_node,
                       min_width=MIN_WINDOW_WIDTH,
                       min_height=MIN_WINDOW_HEIGHT):
    if regularize_node.overlap:
        return False
    if regularize_node is None:
        return False
    # regularize k-d tree
    regularize(regularize_node, border=(2 * WinBorder, WinBorder * 2))

    # load k-d tree
    a, b, reach_size_limit = getLayoutAndKey(
        regularize_node, min_width=min_width, min_height=min_height)
    if reach_size_limit:
        return False
    arrange(a, b)
    return True


def insert_focused_window_into_kdtree(newwin=None):
    if newwin is None:
        active = windowlist.get_active_window()
    else:
        active = newwin
    if active is None:
        return False
    last_active = get_last_active_window()
    if last_active is None:
        return False
    return insert_window_into_kdtree(active, last_active)


def get_last_active_window():
    # assert window list is in stacking order
    assert windowlist.get_active_window(
    ) == windowlist.windowInCurrentWorkspaceInStackingOrder[-1]
    if len(windowlist.windowInCurrentWorkspaceInStackingOrder) > 1:
        return windowlist.windowInCurrentWorkspaceInStackingOrder[-2]
    else:
        return None


def detect_overlap():
    current_layout = windowlist.get_current_layout()
    return getkdtree(windowlist.windowInCurrentWorkspaceInStackingOrder, current_layout)[0].overlap


def find_kdtree(center, target, allow_parent_sibling=True):
    '''
    Adjust non-overlapping layout.
    '''
    active = center

    if None == active:
        return None

    winlist = windowlist.windowInCurrentWorkspaceInStackingOrder

    if active not in winlist:
        return None
    lay = windowlist.get_current_layout()
    _tree, _map = getkdtree(winlist, lay)
    current_node = _map[active]

    if len(current_node.path) % 2 == 0:
        promote = target in ['right', 'left']
    else:
        promote = target in ['down', 'up']

    shift = -1 if target in ['left', 'up'] else 1

    promoted = False

    c = current_node
    if promote:
        c = c.parent
        promoted = True

    while True:
        i = c.parent.children.index(c)
        if 0 <= i + shift < len(c.parent.children):
            target = c.parent.children[i + shift]
            break
        if None == c.parent.parent or None == c.parent.parent.parent:
            return None
        c = c.parent.parent
        promoted = True

    if promoted:
        if not allow_parent_sibling:
            if not target.leaf:
                return None
    if None == target or target.overlap:
        return None
    else:
        return target.key

