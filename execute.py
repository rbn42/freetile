#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import subprocess

import time


def execute_and_output(cmd):
    ENCODING = 'utf8'
    t0 = time.time()
    s = subprocess.check_output(cmd, shell=True).decode(ENCODING)
    t1 = time.time()
#    print('%s:%s' % (t1 - t0, cmd))
    return s


def execute(cmd):
    # print(cmd)
    t0 = time.time()
    os.system(cmd)
    t1 = time.time()
    #print('%s:%s' % (t1 - t0, cmd))
