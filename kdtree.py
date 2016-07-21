#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from divide import divide
import config
import logging


def kdtree(_input, path=None, treemap=None, parentmeta=None, parent=None):
    """
    Build up a k-d tree.
    """
    _input = [n for n in _input]
    if None == treemap:
        # root
        treemap = {}
        path = []

    node = Node()
    node.parent = parent
    node.path = path
    depth = len(path)

    if len(_input) < 2:
        node.leaf = True
        node.overlap = False
        node.content = _input
        node.key = _input[0][1]
    else:

        _input2 = [[pos[depth % 2], pos[depth % 2 + 2]]
                   for pos, _ in _input]  # column first
        children = divide(zip(_input2, _input))

        if len(children) < 2 and depth > 0:
            node.leaf = True
            node.overlap = True
            node.content = _input
        else:

            node.leaf = False
            node.children = []
            for child, i in zip(children, range(len(children))):
                children_path = path + [i]
                _list = [i[1] for i in child]

                node_child = kdtree(_list, path=children_path,
                                    treemap=treemap, parent=node)
                node.children.append(node_child)

                if node_child.overlap:
                    node.overlap = True

    if node.leaf:
        for pos, key in node.content:
            treemap[key] = node
        children_pos = [pos for pos, key in node.content]
    else:
        children_pos = [_child.position for _child in node.children]
        node.key = node.children[0].key

    minx, miny = 10**6, 10**6
    maxx, maxy = -10**6, -10**6
    for pos in children_pos:
        minx = min(minx, pos[0])
        miny = min(miny, pos[1])
        maxx = max(maxx, pos[2])
        maxy = max(maxy, pos[3])
    node.position = [minx, miny, maxx, maxy]

    if 0 == depth:
        _node = Node()
        _node.position = [i for i in node.position]
        _node.overlap = node.overlap
        _node.path = [0]
        _node.children = [node]
        node.parent = _node

        __node = Node()
        __node.position = [i for i in node.position]
        __node.overlap = node.overlap
        __node.path = []
        __node.children = [_node]
        _node.parent = __node

        return __node, treemap
    else:
        return node


def create_parent(node):
    parent = Node()
    parent.parent = node.parent
    node.parent = parent
    parent.overlap = node.overlap
    parent.position = [i for i in node.position]
    parent.path = node.path
    parent.children = [node]
    index = parent.parent.children.index(node)
    parent.parent.children[index] = parent
    return parent


def create_sibling(node):
    sibling = Node()
    sibling.parent = node.parent
    sibling.position = [i for i in node.position]
    i = node.parent.children.index(node)
    node.parent.children.insert(i + 1, sibling)
    return sibling


class Node:
    parent = None
    path = None
    children = None
    key = None
    leaf = None
    overlap = None
    position = None
    content = None
    modified = False

    def __str__(self):
        msg = self.path, self.leaf, self.overlap, self.position, self.content,
        return ",".join([str(i) for i in msg])


def regularize(node, border):
    """
    Regularize a branch in a k-d tree. A node's position is a rectangle defined by x0,y0,x1,y1. All the children's positions will be adjusted to fit exactly to their parents.
    """
    x0, y0, x1, y1 = node.position
    if node.leaf:
        return
    for child in node.children:
        if len(node.path) % 2 == 0:
            child.position[1], child.position[3] = y0, y1
        else:
            child.position[0], child.position[2] = x0, x1
    if len(node.path) % 2 == 0:
        i0, i1, b = x0, x1, border[0]
        index0, index1 = 0, 2
    else:
        i0, i1, b = y0, y1, border[1]
        index0, index1 = 1, 3

    modified_by_user = False
    modified_index = -1
    for child, i in zip(node.children, range(len(node.children))):
        if child.modified:
            modified_index = i
            modified_by_user = True

    i0 = i0 - b
    size = i1 - i0 - len(node.children) * b
    size_sum = 0
    for child, i in zip(node.children, range(len(node.children))):
        if i > modified_index or 1 + modified_index == len(node.children) and not child.modified:
            size_sum += child.position[index1] - child.position[index0]
        else:
            size -= child.position[index1] - child.position[index0]

    i = i0
    for child, index in zip(node.children, range(len(node.children))):
        i += b
        if size == size_sum:
            _size = child.position[index1] - child.position[index0]
        elif modified_by_user:
            assert len(node.children) > 1
            _size = child.position[index1] - child.position[index0]
            # if not child.modified:
            if index > modified_index:
                _size = _size * size / size_sum
                _size = int(_size)
            if modified_index + 1 == len(node.children) and not child.modified:
                _size = _size * size / size_sum
                _size = int(_size)
        else:
            _size = int(size) / len(node.children)
        child.position[index0] = i
        i += _size
        child.position[index1] = i
    node.children[-1].position[index1] = i1

    for child, i in zip(node.children, range(len(node.children))):
        child.path = node.path + [i]
        regularize(child, border)
    return


def remove_single_child_node(node):
    """
    Remove a node from a k-d tree
    """
    if node.leaf:
        return
    l = []
    if len(node.children) == 1:
        child = node.children[0]
        if not child.leaf:
            if not None == node.parent:
                i = node.parent.children.index(node)
                node.parent.children.remove(node)
                for grandchild in child.children:
                    node.parent.children.insert(i, grandchild)
                    grandchild.parent = node.parent
                    i += 1
            l = child.children
    else:
        l = node.children
    for child in l:
        remove_single_child_node(child)


def getLayoutAndKey(node, result=None, min_width=config.MIN_WINDOW_WIDTH, min_height=config.MIN_WINDOW_HEIGHT):
    """
    Extract layouts and window ids from a k-d tree.
    """
    if None == result:
        reach_size_limit = False
        result = [[], [], reach_size_limit]
    if node.leaf:
        x0, y0, x1, y1 = node.position
        if x1 - x0 < min_width or y1 - y0 < min_height:
            #("reach min size")
            result[2] = True
            return result
        layout = [x0, y0, x1 - x0, y1 - y0]
        result[0].append(layout)
        result[1].append(node.key)
    else:
        for child in node.children:
            getLayoutAndKey(child, result)
            if result[2]:
                return result
    return result
