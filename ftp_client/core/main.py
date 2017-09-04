#!/usr/bin/env python
# -*- coding:utf-8 -*-
#----------------------------------------------
#@version:    ??
#@author:   Dylan_wu
#@software:    PyCharm
#@file:    main.py
#@time:    2017/6/20 22:16
#----------------------------------------------
from socket import *
from conf.settings import *
import subprocess
import json
import struct
import os
import sys
import hashlib


def run():
    while True:
        c = socket(AF_INET,SOCK_STREAM)
        c.connect(('127.0.0.1',8080))
        while True:
            username = input('请输入用户名：').strip()
            if not username:continue
            c.sendall(struct.pack('i',len(username)))
            c.sendall(username.encode('utf-8'))
            auth_msg = c.recv(1024).decode('utf-8')
            if auth_msg == '用户验证通过':
                passwd = input('请输入密码：').strip()
                if not passwd:continue
                c.sendall(struct.pack('i', len(passwd)))
                c.sendall(passwd.encode('utf-8'))
                auth_msg = c.recv(1024).decode('utf-8')
                if auth_msg == '验证通过':
                    while True:
                        cmd = input('>').strip()
                        if not cmd: continue
                        if cmd == 'quit':
                            exit()
                        elif cmd.startswith('put'):
                            filepath = cmd.split()[1]
                            # c.send(cmd.encode('utf-8'))

                            if os.path.isfile(filepath):
                                c.send(cmd.encode('utf-8'))
                                filesize = os.stat(filepath).st_size
                                with open(filepath, 'rb') as f:
                                    m = hashlib.md5()
                                    for line in f:
                                        m.update(line)
                                filename = os.path.basename(filepath)
                                hash_num = m.hexdigest()

                                head_dic = {'filename': filename, 'hash': hash_num, 'total_size': filesize}
                                head_json = json.dumps(head_dic)
                                head_bytes = head_json.encode('utf-8')

                                # 先发送报头的长度
                                c.send(struct.pack('i', len(head_bytes)))

                                # 再发送报头的bytes
                                c.send(head_bytes)

                                # 最后发送真实的数据
                                with open(filepath, 'rb') as f:
                                    for line in f:
                                        c.send(line)
                                        send_size = f.tell()
                                        progress(send_size, filesize, '上传中')
                                finish_msg = c.recv(1024)
                                print(finish_msg.decode('utf-8'))
                            else:
                                c.send('put wrong'.encode('utf-8'))
                                print('文件不存在！')
                                continue

                        elif cmd.startswith('get'):
                            c.send(cmd.encode('utf-8'))
                            isfile = c.recv(1024).decode('utf-8')
                            if isfile == 'isfile':
                                head_struct = c.recv(4)
                                head_len = struct.unpack('i', head_struct)[0]
                                head_json = c.recv(head_len).decode('utf-8')
                                head_dict = json.loads(head_json)
                                # print(head_dict)
                                total_size = head_dict['total_size']
                                recv_size = 0
                                recv_data = b''
                                while recv_size < total_size:
                                    once_data = c.recv(10240)
                                    recv_data += once_data
                                    recv_size += len(once_data)
                                    progress(recv_size, total_size, '下载中')

                                filename = head_dict['filename']
                                hash_num = head_dict['hash']
                                # print(filename)
                                with open(os.path.join(os.pardir, Down_load_dir, filename), 'wb') as f:
                                    f.write(recv_data)
                                    f.seek(0)
                                    with open(os.path.join(os.pardir, Down_load_dir, filename), 'rb') as f2:
                                        data = f2.read()
                                m = hashlib.md5()
                                m.update(data)
                                get_file_hash_num = m.hexdigest()
                                if hash_num == get_file_hash_num:
                                    print('文件校验一致，下载成功！')
                                else:
                                    print('文件校验不一致，请重新下载！')
                            else:
                                print(isfile)
                                continue
                        else:
                            c.send(cmd.encode('utf-8'))
                            head_struct = c.recv(4)
                            head_len = struct.unpack('i', head_struct)[0]
                            head_json = c.recv(head_len).decode('utf-8')
                            head_dict = json.loads(head_json)
                            # print(head_dict)
                            total_size = head_dict['total_size']
                            recv_size = 0
                            recv_data = b''
                            while recv_size < total_size:
                                once_data = c.recv(1024)
                                recv_data += once_data
                                recv_size += len(once_data)
                                print(recv_data.decode('utf-8'))
                else:
                    print(auth_msg)
            else:
                print(auth_msg)

    c.close()


def progress( trans_size, file_size, mode):
    '''
    显示进度条
    trans_size: 已经传输的数据大小
    file_size: 文件的总大小
    mode: 模式
    '''
    bar_length = 50  # 进度条长度
    percent = float(trans_size) / float(file_size)
    hashes = '=' * int(percent * bar_length)  # 进度条显示的数量长度百分比
    spaces = ' ' * (bar_length - len(hashes))  # 定义空格的数量=总长度-显示长度
    sys.stdout.write(
        "\r%s:%.2fM/%.2fM %d%% [%s]" % (
        mode, trans_size / 1048576, file_size / 1048576, percent * 100, hashes + spaces))
    sys.stdout.flush()