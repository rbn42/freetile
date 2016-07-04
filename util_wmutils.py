from execute import execute_and_output, execute
import struct


def focus(windowid):
    command = 'wtf %s' % hex(windowid)
    execute(command)
