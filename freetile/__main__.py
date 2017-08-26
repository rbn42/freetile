"""
Freely Tiling Script for X

Usage:
  freetile [options] regularize
  freetile [options] (focus|move|swap) (up|down|left|right)
  freetile [options] (grow|shrink) (height|width)
  freetile [options] autotile
  freetile -h | --help

Options:
  -h --help     Show this screen.
  --debug       Debug
"""
import logging
from docopt import docopt
from freetile.main import *


def main():

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
    elif arguments['autotile']:
        import freetile.auto
        freetile.auto.loop()


if '__main__' == __name__:
    main()
