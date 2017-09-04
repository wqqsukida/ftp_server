#!/usr/bin/env python
# -*- coding:utf-8 -*-
#----------------------------------------------
#@version:    ??
#@author:   Dylan_wu
#@software:    PyCharm
#@file:    Bases.py
#@time:    2017/6/20 22:16
#----------------------------------------------
# from socket import *
import os
import sys
import subprocess
import json
import struct
import hashlib
import socketserver
base_path = os.path.normpath(os.path.join(__file__,os.pardir,os.pardir))
sys.path.insert(0,base_path)

class Ftpserver(socketserver.BaseRequestHandler):
    def handle(self):
    # def __init__(self):
    #     self.server = socket(AF_INET,SOCK_STREAM)
    #     self.server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    #     self.server.bind(('127.0.0.1',8088))
    #     self.server.listen(5)
    #     while True: # 连接循环
            try:
                # print('waiting for connect....')
                self.conn = self.request
                self.client_addr = self.client_address
                print('已经建立连接，正在等待用户验证！')
                while True:
                    first_msg = self.conn.recv(4)# 认证循环
                    if not first_msg:break
                    username_len = struct.unpack('i',first_msg)[0]
                    username = self.conn.recv(username_len).decode('utf-8')
                    os.chdir(sys.path[0]) # 回到根目录
                    user_file = os.path.normpath(os.path.join('db','%s.json'%username))
                    if os.path.isfile(user_file):
                        self.conn.send('用户验证通过'.encode('utf-8'))
                        passwd_len = struct.unpack('i',self.conn.recv(4))[0]
                        passwd = self.conn.recv(passwd_len).decode('utf-8')
                        m1 = hashlib.md5()
                        m1.update(passwd.encode('utf-8'))
                        recv_hash_num = m1.hexdigest()
                        user_json = json.load(open(os.path.join('db','%s.json'%username),'r'))

                        if username == user_json['username'] and recv_hash_num == user_json['password']:
                            self.conn.send('验证通过'.encode('utf-8'))
                            print('客户端：%s 连接成功'%str(self.client_addr))
                            self.path = os.path.join(sys.path[0],'home',username) #  切换用户家目录
                            while True: #　交互循环
                                    cmd = self.conn.recv(1024).decode('utf-8')
                                    print(cmd)
                                    if not cmd:break
                                    if hasattr(self,cmd):
                                        sub_res = getattr(self,cmd)()
                                        if sub_res.stderr.read():
                                            cmd_res = sub_res.stderr.read().decode('gbk').encode('utf-8')
                                        else:
                                            cmd_res = sub_res.stdout.read().decode('gbk').encode('utf-8')
                                        filename = None
                                        hash_num = None
                                    elif cmd.strip() == 'pwd':
                                        cmd_res = self.path.encode('utf-8')
                                        filename = None
                                        hash_num = None

                                    elif cmd.startswith('get') :
                                        filepath = os.path.join(self.path,cmd.split()[1])
                                        if os.path.isfile(filepath):
                                            self.conn.send('isfile'.encode('utf-8'))
                                            cmd_res = self.get_file(filepath)
                                            filename = os.path.basename(filepath)
                                            m = hashlib.md5()
                                            m.update(cmd_res)
                                            hash_num = m.hexdigest()
                                        else:
                                            self.conn.send('文件不存在！'.encode('utf-8'))
                                            continue

                                    elif cmd.startswith('put'):
                                        filepath = cmd.split()[1]
                                        if filepath == 'wrong':continue
                                        head_struct = self.conn.recv(4)
                                        head_len = struct.unpack('i', head_struct)[0]
                                        head_json = self.conn.recv(head_len).decode('utf-8')
                                        head_dict = json.loads(head_json)
                                        # print(head_dict)
                                        total_size = head_dict['total_size']
                                        recv_size = 0
                                        recv_data = b''
                                        while recv_size < total_size:
                                            once_data = self.conn.recv(1024)
                                            recv_data += once_data
                                            recv_size += len(once_data)
                                        filename = head_dict['filename']
                                        hash_num = head_dict['hash']
                                        # print(recv_data.decode('utf-8'))
                                        with open(os.path.join(self.path,filename),'wb') as f:
                                            f.write(recv_data)
                                            f.seek(0)
                                            with open(os.path.join(self.path,filename),'rb') as f2:
                                                data = f2.read()
                                        m = hashlib.md5()
                                        m.update(data)
                                        put_file_hash_num = m.hexdigest()
                                        if  hash_num == put_file_hash_num:
                                            self.conn.send('哈希校验一致，上传完成！'.encode('utf-8'))
                                        else:
                                            self.conn.send('上传文件缺失，请重新上传！'.encode('utf-8'))

                                        continue
                                        # else:
                                        #     continue
                                    else:
                                        cmd_res = '错误的命令！'.encode('utf-8')
                                        filename = None
                                        hash_num = None
                                    head_dic = {'filename': filename, 'hash': hash_num, 'total_size': len(cmd_res)}
                                    head_json = json.dumps(head_dic)
                                    head_bytes = head_json.encode('utf-8')

                                    # 先发送报头的长度
                                    self.conn.send(struct.pack('i', len(head_bytes)))

                                    # 再发送报头的bytes
                                    self.conn.send(head_bytes)

                                    # 最后发送真实的数据
                                    self.conn.send(cmd_res)
                        else:
                            self.conn.send('验证失败'.encode('utf-8'))

                    else:
                        self.conn.send('用户信息不存在，请重新登录！'.encode('utf-8'))

            except ConnectionResetError as e:
                print(e)
                # break
    def chr_dir(self,username):
        os.chdir(os.path.normpath(os.path.join('home', username)))


    def get_file(self,filename):
            with open(filename,'rb') as f:
                file_data = f.read()
            return file_data


    def put_file(self):
        self.conn.send('put'.encode('utf-8'))

    def dir(self):
        dir_res = subprocess.Popen('dir %s'%self.path,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return dir_res

    # def pwd(self):
    #     pwd_res = subprocess.Popen('cd', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     return pwd_res

if __name__ == '__main__':
        socketserver.TCPServer.allow_reuse_address = True
        s = socketserver.ThreadingTCPServer(('127.0.0.1', 8080), Ftpserver)
        s.serve_forever()  # 链接循环