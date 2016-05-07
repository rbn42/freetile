from execute import execute_and_output, execute
import re


def get_screensize():
    cmd = 'xrandr'
    out = execute_and_output(cmd)
    l = re.findall('current\s?(\d+)\s?x\s?(\d+)', out)
    w, h = l[0]
    return int(w), int(h)
if __name__ == '__main__':
    print(get_screensize())
