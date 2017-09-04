#!/usr/bin/env python
# -*- coding:utf-8 -*-
#----------------------------------------------
#@version:    ??
#@author:   Dylan_wu
#@software:    PyCharm
#@file:    start.py
#@time:    2017/6/20 21:56
#----------------------------------------------

import os
import sys

base_path = os.path.normpath(os.path.join(__file__,os.pardir,os.pardir))
sys.path.insert(0,base_path)

from core import main

if __name__ == '__main__':
    main.run()
