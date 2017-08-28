#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import json

from .divide import divide


class Node:
    """
    Build up a 2d tree.
    """
    parent = None
    children = None
    key = None
    position = None
    """node resized by user"""
    resized = False
    DIMENSION = 2
    __leafnodemap = None

    def __str__(self):
        obj = self.to_json()
        return json.dumps(obj, indent=4, sort_keys=True)

    def to_json(self):
        return {
            '1.key': self.key,
            '2.position': self.position,
            '3.resized': self.resized,
            '4.children': [
                child.to_json() for child in self.children] if self.children else None,
        }

    def leaf(self):
        return self.children is None

    def leafnodemap(self):
        if self.parent is None:
            # root
            return self.__leafnodemap
        else:
            return self.parent.leafnodemap()

    def dimension(self):
        """
        The dimension expected to be controlled by current node and divided between children.
        """
        # column first
        index_min = self.depth() % self.DIMENSION
        index_max = self.depth() % self.DIMENSION + self.DIMENSION
        return index_min, index_max

    def targets(self):
        dmin, dmax = self.parent.dimension()
        if dmin == 0:
            return 'left', 'right'
        elif dmin == 1:
            return 'up', 'down'

    def interval_size(self):
        dmin, dmax = self.parent.dimension()
        return self.position[dmax] - self.position[dmin]

    def __init__(self, _input, parent=None):
        # create empty node
        if _input is None:
            return
        if parent is None:
            # root
            self.__leafnodemap = {}
        else:
            self.parent = parent

        if len(_input) == 1:
            pos, key = _input[0]
            self.key = key
            self.leafnodemap()[key] = self
        else:
            dmin, dmax = self.dimension()
            _input2 = [[pos[dmin], pos[dmax]] for pos, v in _input]
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

    def init_position(self, _input=None):
        if self.leaf():
            position_children = [position for position, value in _input]
        else:
            position_children = [child.position for child in self.children]
        minx, miny = 10**6, 10**6
        maxx, maxy = -10**6, -10**6
        minx = min([pos[0] for pos in position_children])
        miny = min([pos[1] for pos in position_children])
        maxx = max([pos[2] for pos in position_children])
        maxy = max([pos[3] for pos in position_children])
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
        else:
            # root
            new_parent.__leafnodemap = self.__leafnodemap

        self.parent = new_parent

        return new_parent

    def create_sibling(self):
        sibling = Node(None)
        sibling.parent = self.parent
        sibling.position = list(self.position)

        index = self.parent.children.index(self)
        self.parent.children.insert(index + 1, sibling)
        return sibling

    def children_resized(self, gap):
        dmin, dmax = self.dimension()
        start = self.position[dmin]
        end = self.position[dmax]
        gap = gap[dmin]
        size = len(self.children)
        interval = int((end - start + gap) / size) - gap
        i = start
        for index in range(size):
            child = self.children[index]
            min_expect = i
            max_expect = i + interval
            i += interval + gap
            if index == size - 1:
                max_expect = end
            cmin = child.position[dmin]
            cmax = child.position[dmax]
            if not cmin == min_expect or not cmax == max_expect:
                return True
        return False

    def regularize(self, gap):
        """
        Regularize a branch in a 2d tree. A node's position is a rectangle
        defined by x0,y0,x1,y1. All the children's positions will be adjusted
        to fit exactly to their parents.
        """
        if self.leaf():
            return
        dmin, dmax = self.dimension()

        for child in self.children:
            for i in range(2 * self.DIMENSION):
                if i not in [dmin, dmax]:
                    child.position[i] = self.position[i]
        i0 = self.position[dmin]
        i1 = self.position[dmax]
        b = gap[dmin]
        num = len(self.children)

        resizeed_index = -1
        for i in range(num):
            child = self.children[i]
            if child.resized:
                resizeed_index = i

        i0 = i0 - b
        size = i1 - i0 - num * b
        size_sum = 0
        if resizeed_index < 0:
            for child in self.children:
                size_sum += child.interval_size()
            i = i0
            default_interval_size = int(size / num)
            for child in self.children:
                i += b
                if size == size_sum:
                    _size = child.interval_size()
                else:
                    _size = default_interval_size
                    # _size += int(child.interval_size() * size / size_sum)
                child.position[dmin] = i
                i += _size
                child.position[dmax] = i
        else:
            for i in range(num):
                child = self.children[i]
                if i > resizeed_index \
                        or 1 + resizeed_index == num \
                        and not child.resized:
                    size_sum += child.interval_size()
                else:
                    size -= child.interval_size()

            i = i0
            for index in range(num):
                child = self.children[index]
                i += b
                if size == size_sum:
                    _size = child.interval_size()
                else:
                    _size = child.interval_size()
                    if index > resizeed_index or resizeed_index + \
                            1 == num and not child.resized:
                        _size = int(_size * size / size_sum)
                child.position[dmin] = i
                i += _size
                child.position[dmax] = i

        self.children[-1].position[dmax] = self.position[dmax]
        for child, i in zip(self.children, range(len(self.children))):
            child.regularize(gap)

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

    def getLayout(self, size_limit_map):
        """
        Extract layouts and window ids from a 2d tree.
        """
        if self.children is None:
            x0, y0, x1, y1 = self.position
            minw, minh = size_limit_map[self.key]
            layout = [x0, y0, x1 - x0, y1 - y0]
            return [layout], [self.key], x1 - x0 < minw or y1 - y0 < minh
        else:
            layouts, values, reach_size_limit = [], [], False
            for child in self.children:
                l, v, r, = child.getLayout(size_limit_map)
                layouts += l
                values += v
                reach_size_limit = reach_size_limit or r
            return layouts, values, reach_size_limit


if __name__ == '__main__':
    print('test')
