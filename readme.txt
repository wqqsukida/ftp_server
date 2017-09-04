一,关于ftp(socketserver并发实现)：
    （请在pycharm 2016.1.2下运行，其他版本进度条显示可能有问题）
    1.先运行ftp_server/bin/下的start.py,再运行ftp_client/bin/下的start.py（可同时运行多个客户端）
    2.两个账号：
        elaine 密码：456   家目录：ftp_server/home/elaine
        dylan  密码：123   家目录：ftp_server/home/dylan
    3.进入后可使用以下命令：
         dir：查看当前目录下的文件
         pwd：显示当前路径
         get filepath: 下载文件（下载到settings下的Down_load_dir,默认为ftp_client/down_load）
         put filepath: 上传文件（上传至用户家目录)
         quit：退出
    4.问题：
        -目前在除了pycharm的其他终端运行，下载上传进度条显示可能有问题
        -windows cmd和linux下运行，登录加密验证会有严重错误！！！：
            **如：第一次用户验证失败，会导致再次登录即使输入正确密码也会失败
            考虑到可能是因为粘包问题造成，分别在客户端发送账号密码时加入了4个字节的头部信息
            保证服务端接受账号密码正确，但依旧有问题，目前无法解决**

二,博客地址：http://www.cnblogs.com/dylan-wu/articles/7106782.html