import re
import subprocess
from ..config import EMACS_NAVIGATION_CMD, EMACS_WINDOW_NAME

debug = False


def navigate(window_name, target_direction):
    if EMACS_WINDOW_NAME is not None:
        if debug:
            print('start')
        l = re.findall(EMACS_WINDOW_NAME, window_name)
        if debug:
            print(l)
        if len(l) > 0:
            cmd = EMACS_NAVIGATION_CMD.format(target=target_direction)
            try:
                s = subprocess.check_output(cmd, shell=True).decode('utf8')
            except BaseException:
                return False
            if debug:
                print(s)
            if 'nil' == s.strip():
                return True
    return False


if '__main__' == __name__:
    EMACS_WINDOW_NAME = ".+emacs.+"
    EMACS_NAVIGATION_CMD = "emacsclient -e '(evil-window-{target} 1)'"
    debug = True
    print('window name:')
    name = input().strip()
    print('direction:')
    target = input().strip()
    print(navigate(name, target))
