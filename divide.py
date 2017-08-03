#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def divide(_input):
    '''
    divide intervals
    '''
    # find out separable intervals
    _input = sorted([n for n in _input])
    l = [interval for interval, value in _input]
    for i0, i1 in l:
        assert not i0 == i1
    current_start, current_end = None, None
    result = []
    for start, end in l:  # zip(l[:-1], l[1:]):
        if current_start is None:
            current_start, current_end = start, end
        else:
            if start >= current_end:
                result.append((current_start, current_end))
                current_start, current_end = start, end
            else:
                current_end = max(end, current_end)
    result.append((current_start, current_end))

    nodes = result
    # assign children to intervals
    children = []
    l = []
    current_start, current_end = nodes.pop(0)
    for child in _input:
        interval, value = child
        start, end = interval
        if not end <= current_end:
            children.append(l)
            current_start, current_end = nodes.pop(0)
            l = []
        l.append(child)
    children.append(l)

    return children


if __name__ == '__main__':
    _input = [[0.3, 0.4], [0.2, 0.5], [0.6, 0.8], [0.8, 0.9], [0.8, 1.0]]
    _input = list(zip(_input, range(len(_input))))
    # print(_input)
    _out = [[([0.2, 0.5], 1), ([0.3, 0.4], 0)], [([0.6, 0.8], 2)],
            [([0.8, 0.9], 3), ([0.8, 1.0], 4)]]
    try:
        assert divide(_input) == _out
    except BaseException:
        print(divide(_input))

    _input = [[-0.1, 0.4], [0.3, 0.4],
              [0.2, 0.5], [0.6, 0.8], [0.8, 0.9], [0.8, 1.0]]
    _input = list(zip(_input, range(len(_input))))
    _out = [[([-0.1, 0.4], 0), ([0.2, 0.5], 2), ([0.3, 0.4], 1), ], [
        ([0.6, 0.8], 3)], [([0.8, 0.9], 4), ([0.8, 1.0], 5)]]

    try:
        assert divide(_input) == _out
    except BaseException:
        print(divide(_input))
    # print(divide(_input))
    # print(_input)
    _input = [[-0.1, 0.4], [1.1, 1.2], [0.3, 0.4],
              [0.2, 0.5], [0.6, 0.8], [0.8, 0.9], [0.8, 1.0]]
    _input = list(zip(_input, range(len(_input))))
    # print(_input)
    print(divide(_input))
