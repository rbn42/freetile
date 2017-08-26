"""
Freely Tiling Script for X

Usage:
  freetile [options] tile
  freetile [options] (focus|move|swap) (up|down|left|right)
  freetile [options] (grow|shrink) (height|width)
  freetile [options] autotile
  freetile [options] test
  freetile -h | --help

Options:
  -h --help     Show this screen.
  --debug       Debug
"""
import logging
from docopt import docopt
from freetile.main import swap, move, regularize, focus, grow_width, grow_height, shrink_width, shrink_height
from freetile.windowlist import windowlist


def main():
    arguments = docopt(__doc__)

    if arguments['--debug']:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
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
    elif arguments['tile']:
        regularize()
    elif arguments['grow']:
        if arguments['width']:
            grow_width()
        else:
            grow_height()
    elif arguments['shrink']:
        if arguments['width']:
            shrink_width()
        else:
            shrink_height()
    elif arguments['autotile']:
        from freetile.auto import loop
        loop()
    elif arguments['test']:
        from freetile.test import main
        main()


if '__main__' == __name__:
    main()
