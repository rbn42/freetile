#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import subprocess


def execute_and_output(cmd):
    ENCODING = 'utf8'
    return subprocess.check_output(cmd, shell=True).decode(ENCODING)


def execute(cmd):
    # print(cmd)
    os.system(cmd)