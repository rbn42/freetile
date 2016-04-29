#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def divide(_input):
    _input=[n for n in _input]
    _input.sort()
    l = [i for i, j in _input]

    l += [[1.0, 1.1], [1.3, 1.4]]
    result = []
    _min, _max = -0.1, 0.0
    for i0, i1 in l:
        assert not i0 == i1
        if i0 >= _max:
            if _max > _min:
                result.append([_min, _max])
            _min, _max = i0, i1
        elif i1 > _max:
            _max = i1
    l = result
    result = [[i0[1], i1[0]] for i0, i1 in zip(l[:-1], l[1:])]
    nodes = [i0 + i1 for i0, i1 in zip(result[:-1], result[1:])]
    ######################
    children = []
    n = nodes.pop(0)
    l = []
    for child in _input:
        if not child[0][0] < n[-1]:
            children.append(l)
            n = nodes.pop(0)
            l = []
        l.append(child)
    children.append(l)

    return children

if __name__ == '__main__':
    _input = [[0.3, 0.4], [0.2, 0.5], [0.6, 0.8], [0.8, 0.9], [0.8, 1.0]]
    _input = list(zip(_input, range(len(_input))))
    divide(_input)
