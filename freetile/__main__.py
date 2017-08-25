#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Window tiling for X

Usage:
  main.py [options] regularize
  main.py [options] (focus|move|swap) (up|down|left|right)
  main.py [options] (grow|shrink) (height|width)
  main.py -h | --help

Options:
  -h --help     Show this screen.
  --debug       Debug
"""
import logging
from docopt import docopt

if '__main__' == __name__:
    arguments = docopt(__doc__)

    if arguments['--debug']:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        )
    else:
        logging.basicConfig(level=logging.INFO)

    for target in ('up', 'down', 'left', 'right'):
        if arguments[target]:
            break

    from .main import *
    windowlist.reset()

    if arguments['swap']:
        swap(target)
    elif arguments['move']:
        move(target)
    elif arguments['focus']:
        focus(target)
    elif arguments['regularize']:
        regularize()
    elif arguments['grow']:
        if arguments['width']:
            resize(config.RESIZE_STEP, 0)
        else:
            resize(0, config.RESIZE_STEP)
    elif arguments['shrink']:
        if arguments['width']:
            resize(-config.RESIZE_STEP, 0)
        else:
            resize(0, -config.RESIZE_STEP)
