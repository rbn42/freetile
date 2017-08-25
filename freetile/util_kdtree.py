import logging
from .config import MAX_KD_TREE_BRANCH, REGULARIZE_FULLSCREEN, WindowGap

from .tree import Node
from .windowlist import windowlist
from .workarea import workarea


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
    _tree = getkdtree(winlist, lay)
    if active not in _tree.leafnodemap():
        return False
    current_node = _tree.leafnodemap()[active]

    # determine the size of current node and parent node.
    if current_node.depth() % 2 == 0:
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
        if not current_node.overlap():
            if current_node.parent is not None:
                node = current_node
                index = index_current
                _resize = resize_current
                node.resized = True
                regularize_node = node.parent
                # invert the operation if the node is the last child of its
                # parent
                if regularize_node.children[-1] == node:
                    node.position[index] -= _resize
                else:
                    node.position[index] += _resize

    if not resize_parent == 0:
        if current_node.parent is not None:
            if not current_node.parent.overlap():
                if current_node.parent.parent is not None:
                    node = current_node.parent
                    index = index_parent
                    _resize = resize_parent
                    node.resized = True
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
        return regularize_kd_tree(_tree, ignore_size_limit_error=True)
    return regularize_kd_tree(regularize_node, ignore_size_limit_error=True)


def getkdtree(winlist, lay):
    origin_lay = [[x, y, x + w, y + h] for x, y, w, h in lay]
    lst = list(zip(origin_lay, winlist))
    return Node(lst).create_parent().create_parent()


def insert_window_into_kdtree(winid, target):
    winlist = [
        w for w in windowlist.windowInCurrentWorkspaceInStackingOrder
        if not w == winid]
    lay = windowlist.get_current_layout()
    _tree = getkdtree(winlist, lay)
    if target not in _tree.leafnodemap():
        # overlapped
        return False
    target_node = _tree.leafnodemap()[target]
    if target_node.parent.children_resized(gap=(WindowGap, WindowGap)):
        # if node is resized by user, dont resize it in the same axis again.
        target_node.create_parent()
    node = target_node.create_sibling()
    node.key = winid
    if REGULARIZE_FULLSCREEN:
        _tree.position = [workarea.x, workarea.y, workarea.x +
                          workarea.width, workarea.y + workarea.height]
        return regularize_kd_tree(_tree, ignore_size_limit_error=True)
    return regularize_kd_tree(node.parent, ignore_size_limit_error=True)


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
    _tree = getkdtree(winlist, lay)
    if active not in _tree.leafnodemap():
        return False
    current_node = _tree.leafnodemap()[active]

    # whether promote node to its parent's level
    if current_node.depth() % 2 == 0:
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
                if new_parent.leaf() and not _swap:
                    # But allow no more than one branch for each node
                    non_leaf_node_count = 0
                    for sibling in new_parent.parent.children:
                        if not sibling.leaf() or MAX_KD_TREE_BRANCH < 1:
                            non_leaf_node_count += 1
                            if not non_leaf_node_count < MAX_KD_TREE_BRANCH:
                                # Just swap them.
                                _swap = True
                                break
                    else:
                        new_parent = new_parent.create_parent()
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
    regularize_node.remove_from_tree()

    if regularize_node.overlap():
        return False

    # regularize k-d tree
    regularize_node = regularize_node.parent
    if REGULARIZE_FULLSCREEN:
        _tree.position = [workarea.x, workarea.y, workarea.x +
                          workarea.width, workarea.y + workarea.height]
        return regularize_kd_tree(_tree, ignore_size_limit_error=True)
    return regularize_kd_tree(regularize_node, ignore_size_limit_error=True)


def search_for_regularized_windows(_min, _max, stack, layout_stack):
    """
    search for regularized windows from stack bottom
    """
    result = None
    while _min <= _max:
        num = int(_min / 2 + _max / 2)
        winlist = stack[:num]
        layout = layout_stack[:num]
        tree = getkdtree(winlist, layout)
        if tree.overlap():
            _max = num - 1
        else:
            result = tree, winlist, num
            _min = num + 1
    return result


def regularize_or_insert_windows(min_regularized_window):
    stack = windowlist.windowInCurrentWorkspaceInStackingOrder
    layout_stack = windowlist.get_current_layout()
    num = len(stack)

    result = search_for_regularized_windows(
        min_regularized_window, num, stack, layout_stack)
    if result is None:
        return False
    tree, winlist, num = result

    target = winlist[-1]
    target_node = tree.leafnodemap()[target]

    tree.regularize(gap=(WindowGap, WindowGap))

    if target_node.parent.children_resized(gap=(WindowGap, WindowGap)):
        # if node is resized by user, dont resize it in the same axis
        # again.
        target_node.create_parent()
    # add all the rest windows to tree.
    for winid in stack[num:]:
        node = target_node.create_sibling()
        node.key = winid

    if REGULARIZE_FULLSCREEN:
        tree.position = [workarea.x, workarea.y, workarea.x +
                         workarea.width, workarea.y + workarea.height]
    tree.regularize(gap=(WindowGap, WindowGap))
    # load k-d tree
    a, b, reach_size_limit = tree.getLayout(windowlist.minGeometry)
    if reach_size_limit:
        logging.info('reach window minimal size')
        return True
    windowlist.arrange(a, b)
    return True


def regularize_kd_tree(regularize_node,
                       ignore_size_limit_error=False):
    if regularize_node is None:
        return False
    if regularize_node.overlap():
        return False
    # regularize k-d tree
    regularize_node.regularize(gap=(WindowGap, WindowGap))

    # load k-d tree
    a, b, reach_size_limit = regularize_node.getLayout(windowlist.minGeometry)
    if reach_size_limit:
        logging.info('reach window minimal size')
        if ignore_size_limit_error:
            return True
        return False
    windowlist.arrange(a, b)
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
    active = windowlist.get_active_window()
    lst = windowlist.windowInCurrentWorkspaceInStackingOrder
    index = lst.index(active)
    index = (index - 1) % len(lst)
    return lst[index]


def find_kdtree(center, target, allow_parent_sibling=True):
    '''
    Adjust non-overlapping layout.
    '''
    active = center

    if active is None:
        return None

    winlist = windowlist.windowInCurrentWorkspaceInStackingOrder

    if active not in winlist:
        return None
    lay = windowlist.get_current_layout()
    _tree = getkdtree(winlist, lay)
    if active not in _tree.leafnodemap():
        return None
    current_node = _tree.leafnodemap()[active]

    if current_node.depth() % 2 == 0:
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
        if c.parent.parent is None or c.parent.parent.parent is None:
            return None
        c = c.parent.parent
        promoted = True

    if promoted:
        if not allow_parent_sibling:
            if not target.leaf():
                return None
    if target is None or target.overlap():
        return None
    else:
        return target.key
