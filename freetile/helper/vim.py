import re
import subprocess
from ..config import VIM_NAVIGATION_CMD, VIM_SERVER_NAME

debug = False


def navigate(window_name, target_direction):
    if VIM_SERVER_NAME is not None:
        if debug:
            print('start')
        vimserver = re.findall(VIM_SERVER_NAME, window_name)
        if debug:
            print(vimserver)
        if len(vimserver) > 0:
            vimserver = vimserver[0]
            cmd = VIM_NAVIGATION_CMD.format(vimserver=vimserver,
                                            target=target_direction)
            s = subprocess.check_output(cmd, shell=True).decode('utf8')
            if debug:
                print(s)
            s = int(s)
            if s == 1:
                return True
    return False


if '__main__' == __name__:
    VIM_SERVER_NAME = " - (VIMSERVER\d+)$"
    print(VIM_SERVER_NAME)
    print(VIM_NAVIGATION_CMD)
    debug = True
    print('window name:')
    name = input().strip()
    print('direction:')
    target = input().strip()
    print(navigate(name, target))
