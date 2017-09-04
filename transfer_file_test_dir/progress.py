#!/usr/bin/env python
# -*- coding:utf-8 -*-
#----------------------------------------------
#@version:    ??                               
#@author:   Dylan_wu                                                        
#@software:    PyCharm                  
#@file:    progress.py
#@time:    2017/6/23 10:24
#----------------------------------------------
import sys,time
#
# for i in range(50):
#     sys.stdout.write('%s\r' %('#'*i))    # \r 为不换行，跳到行首
#     sys.stdout.flush()
#     time.sleep(0.1)
def progress( trans_size, file_size, mode):
    bar_length = 50
    percent = float(trans_size) / float(file_size)
    hashes = '=' * int(percent * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write(
        "\r%s:[%s]"%(mode,hashes+spaces)
    )
    sys.stdout.flush()
# def progress( trans_size, file_size, mode):
#     '''
#     显示进度条
#     trans_size: 已经传输的数据大小
#     file_size: 文件的总大小
#     mode: 模式
#     '''
#     for trans_size in range(0,file_size,1048):
#         # trans_size += 1048
#         bar_length = 100  # 进度条长度
#         percent = float(trans_size) / float(file_size)
#         hashes = '=' * int(percent * bar_length)  # 进度条显示的数量长度百分比
#         spaces = ' ' * (bar_length - len(hashes))  # 定义空格的数量=总长度-显示长度
#         sys.stdout.write(
#             "\r%s:%.2fM/%.2fM %d%% [%s]" % (
#             mode, trans_size / 1048576, file_size / 1048576, percent * 100, hashes + spaces))
#         sys.stdout.flush()
#
trans_size = 0
file_size = 10485760
mode = '读取中'

while trans_size < file_size:
    trans_size+=1048
    progress(trans_size, file_size, mode)
# progress(trans_size, file_size, mode)