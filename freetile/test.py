"""
"""
import logging
from .windowlist import windowlist
from .workarea import workarea


def main():
    logging.info('Start test')
    logging.debug('load windows info')
    windowlist.reset()

    logging.debug(
        'current work area:%s,%s,%s,%s',
        workarea.x,
        workarea.y,
        workarea.width,
        workarea.height)

    winid = windowlist.windowInCurrentWorkspaceInStackingOrder[-1]
    logging.debug('current active window id:%s', winid)
    geo = windowlist.windowGeometry[winid]
    logging.debug('current active window geo:%s', geo)
    target = [
        workarea.width // 4,
        workarea.height // 4,
        workarea.width // 2,
        workarea.height // 2]
    logging.info(
        "Try to move current window to %d,%d and resize to %dx%d",
        *target)
    windowlist.arrange([target], [winid])
    logging.debug('sleep 1s')
    import time
    time.sleep(1)
    logging.debug('load windows info')
    windowlist.reset()
    winid = windowlist.windowInCurrentWorkspaceInStackingOrder[-1]
    logging.debug('current active window id:%s', winid)
    newgeo = windowlist.windowGeometry[winid]
    logging.info('Current window is moved to %d,%d and resized to %dx%d', *geo)
    if newgeo == target:
        logging.info('Test succeeded')
    else:
        logging.debug('Test failed')
