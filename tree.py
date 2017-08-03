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
    DIMENSION = 2

    def print(self):
        tab = '  ' * self.depth()
        print('%s%s,%s,%s' % (tab,
                              self.key, self.position, self.modified))
        if self.children is not None:
            for child in self.children:
                child.print()

    def leaf(self):
        return self.children is None

    def dimension(self):
        """
        The dimension expected to be controlled by current node and divided between children. 
        """
        # column first
        index_min=self.depth() % self.DIMENSION
        index_max=self.depth() % self.DIMENSION + self.DIMENSION
        return index_min,index_max 

    def targets(self):
        dmin,dmax=self.parent.dimension()
        if dmin == 0:
            return 'left', 'right'
        elif dmin == 1:
            return 'up', 'down'


    def interval_size(self):
        dmin,dmax=self.parent.dimension()
        return self.position[dmax]-self.position[dmin]

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
        dmin, dmax = self.dimension() 

        for child in self.children:
            for i in range(self.DIMENSION):
                if i not in [dmin,dmax]:
                    child.position[i] = self.position[i]
        i0 = self.position[dmin]
        i1 = self.position[dmax]
        b = border[dmin]

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
                size_sum += child.interval_size()
            else:
                size -= child.interval_size()

        i = i0
        for child, index in zip(self.children, range(len(self.children))):
            i += b
            if size == size_sum:
                _size = child.interval_size()
            elif modified_by_user:
                assert len(self.children) > 1
                _size = child.interval_size()
                # if not child.modified:
                if index > modified_index:
                    _size = _size * size / size_sum
                    _size = int(_size)
                if modified_index + 1 == len(self.children) and not child.modified:
                    _size = _size * size / size_sum
                    _size = int(_size)
            else:
                _size = int(size) / len(self.children)
            child.position[dmin] = i
            i += _size
            child.position[dmax] = i
        self.children[-1].position[dmax] = i1

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
                return None, None, True,
            else:
                layout = [int(x0), int(y0), int(x1 - x0), int(y1 - y0)]
                return [layout], [self.key], False,
        else:
            layouts, values = [], []
            for child in self.children:
                l, v, reach_size_limit, = child.getLayout()
                if reach_size_limit:
                    break
                layouts += l
                values += v
            return layouts, values, reach_size_limit


if __name__ == '__main__':
    print('test')
