#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import config

from divide import divide

leafnodemap = {}


class Node:
    """
    Build up a 2d tree.
    """
    parent = None
    children = None
    key = None
    position = None
    modified = False

    def print(self):
        tab = '  ' * self.depth()
        print('%s%s,%s,%s' % (tab,
                              self.key, self.position, self.modified))
        if self.children is not None:
            for child in self.children:
                child.print()

    def leaf(self):
        return self.children is None

    def __init__(self, _input, parent=None):
        # create empty node
        if _input is None:
            return
        self.parent = parent

        if len(_input) == 1:
            pos, key = _input[0]
            self.key = key
            leafnodemap[key] = self
        else:
            _input2 = [[pos[self.depth() % 2], pos[self.depth() % 2 + 2]]
                       for pos, v in _input]  # column first
            intervals = divide(zip(_input2, _input))
            if len(intervals) == 1 and self.depth() > 0:
                pass
            else:
                self.children = []
                for item in intervals:
                    _list = [nodelist for interval, nodelist in item]
                    node_child = Node(_list, parent=self)
                    self.children.append(node_child)

        self.position = self.init_position(_input)

    def init_position(self, _input):
        if self.leaf():
            position_children = [position for position, value in _input]
        else:
            position_children = [child.position for child in self.children]
        minx, miny = 10**6, 10**6
        maxx, maxy = -10**6, -10**6
        minx = min([pos[0] for pos in position_children])
        miny = min([pos[1] for pos in position_children])
        maxx = min([pos[2] for pos in position_children])
        maxy = min([pos[3] for pos in position_children])
        return [min(10**6, minx), min(10**6, miny),
                max(-10**6, maxx), max(-10**6, maxy), ]

    def depth(self):
        if self.parent is None:
            return 0
        return 1 + self.parent.depth()

    def overlap(self):
        if self.leaf():
            return self.key is None

        for child in self.children:
            if child.overlap():
                return True
        return False

    def create_parent(self):
        new_parent = Node(None)
        new_parent.parent = self.parent
        new_parent.children = [self]
        new_parent.position = list(self.position)

        if self.parent is not None:
            index = self.parent.children.index(self)
            self.parent.children[index] = new_parent

        self.parent = new_parent

        return new_parent

    def create_sibling(self):
        sibling = Node(None)
        sibling.parent = self.parent
        sibling.position = list(self.position)

        index = self.parent.children.index(self)
        self.parent.children.insert(index + 1, sibling)
        return sibling

    def regularize(self, border):
        """
        Regularize a branch in a 2d tree. A node's position is a rectangle
        defined by x0,y0,x1,y1. All the children's positions will be adjusted
        to fit exactly to their parents.
        """
        if self.leaf():
            return
        x0, y0, x1, y1 = self.position
        for child in self.children:
            if self.depth() % 2 == 0:
                child.position[1], child.position[3] = y0, y1
            else:
                child.position[0], child.position[2] = x0, x1
        if self.depth() % 2 == 0:
            i0, i1, b = x0, x1, border[0]
            index0, index1 = 0, 2
        else:
            i0, i1, b = y0, y1, border[1]
            index0, index1 = 1, 3

        modified_by_user = False
        modified_index = -1
        for child, i in zip(self.children, range(len(self.children))):
            if child.modified:
                modified_index = i
                modified_by_user = True

        i0 = i0 - b
        size = i1 - i0 - len(self.children) * b
        size_sum = 0
        for child, i in zip(self.children, range(len(self.children))):
            if i > modified_index \
                    or 1 + modified_index == len(self.children) \
                    and not child.modified:
                size_sum += child.position[index1] - child.position[index0]
            else:
                size -= child.position[index1] - child.position[index0]

        i = i0
        for child, index in zip(self.children, range(len(self.children))):
            i += b
            if size == size_sum:
                _size = child.position[index1] - child.position[index0]
            elif modified_by_user:
                assert len(self.children) > 1
                _size = child.position[index1] - child.position[index0]
                # if not child.modified:
                if index > modified_index:
                    _size = _size * size / size_sum
                    _size = int(_size)
                if modified_index + 1 == len(self.children) and not child.modified:
                    _size = _size * size / size_sum
                    _size = int(_size)
            else:
                _size = int(size) / len(self.children)
            child.position[index0] = i
            i += _size
            child.position[index1] = i
        self.children[-1].position[index1] = i1

        for child, i in zip(self.children, range(len(self.children))):
            child.regularize(border)

    def remove_from_tree(self):
        """
        Remove a node from a 2d tree, and keep children.
        """
        if self.children is None:
            return
        l = []
        if len(self.children) == 1:
            child = self.children[0]
            if child.children is not None:
                if self.parent is not None:
                    i = self.parent.children.index(self)
                    self.parent.children.remove(self)
                    for grandchild in child.children:
                        self.parent.children.insert(i, grandchild)
                        grandchild.parent = self.parent
                        i += 1
                l = child.children
        else:
            l = self.children
        for child in l:
            child.remove_from_tree()

    def getLayout(self,
                  min_width=config.MIN_WINDOW_WIDTH,
                  min_height=config.MIN_WINDOW_HEIGHT):
        """
        Extract layouts and window ids from a 2d tree.
        """
        if self.children is None:
            x0, y0, x1, y1 = self.position
            if x1 - x0 < min_width or y1 - y0 < min_height:
                return [], [], True,
            layout = [int(x0), int(y0), int(x1 - x0), int(y1 - y0)]
            return [layout], [self.key], False,
        else:
            layouts, values = [], []
            for child in self.children:
                l, v, reach_size_limit, = child.getLayout()
                layouts += l
                values += v
                if reach_size_limit:
                    return layouts, values, reach_size_limit,
            return layouts, values, False


if __name__ == '__main__':
    print('test')
