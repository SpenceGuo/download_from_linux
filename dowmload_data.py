"""
通过paramiko从远处服务器下载文件资源到本地
author: gxcuizy
time: 2018-08-01
"""

import paramiko
import os
from stat import S_ISDIR as isdir


def down_from_remote(sftp_obj, remote_dir_name, local_dir_name):
    """远程下载文件"""
    remote_file = sftp_obj.stat(remote_dir_name)
    if isdir(remote_file.st_mode):
        # 文件夹，不能直接下载，需要继续循环
        check_local_dir(local_dir_name)
        print('开始下载文件夹：' + remote_dir_name)
        for remote_file_name in sftp.listdir(remote_dir_name):
            sub_remote = os.path.join(remote_dir_name, remote_file_name)
            sub_remote = sub_remote.replace('\\', '/')
            sub_local = os.path.join(local_dir_name, remote_file_name)
            sub_local = sub_local.replace('\\', '/')
            down_from_remote(sftp_obj, sub_remote, sub_local)
    else:
        # 文件，直接下载
        print('开始下载文件：' + remote_dir_name)
        sftp.get(remote_dir_name, local_dir_name)


def check_local_dir(local_dir_name):
    """本地文件夹是否存在，不存在则创建"""
    if not os.path.exists(local_dir_name):
        os.makedirs(local_dir_name)


def get_source_list(file_path: str):
    """
    获取下载资源的路径列表
    :param file_path: 这是列表文件的路径，从列表文件中获取需要下载的资源列表
    :return: 返回所有资源文件列表的路径，以数组形式返回
    """
    path_list = []
    f = open(file_path, "r")
    raw_data = f.read().splitlines()
    for line in raw_data:
        path_list.append(line.split("\t")[1])
    f.close()
    return path_list


if __name__ == "__main__":
    """程序主入口"""
    # 服务器连接信息
    host_name = '10.10.10.10'
    user_name = 'your username'
    password = 'your password'
    port = 22
    # 连接远程服务器
    t = paramiko.Transport((host_name, port))
    t.connect(username=user_name, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)

    # 远程文件路径（需要绝对路径）
    source_list = get_source_list("source_data/id_pdf_path.txt")
    # remote_dir = ""
    # # 本地文件存放路径（绝对路径或者相对路径都可以）
    # local_dir = 'download_data/'

    for path in source_list:
        remote_dir = path
        local_dir = 'download_data/'
        local_dir = local_dir + path.split("/")[-1]
        # 远程文件开始下载
        down_from_remote(sftp, remote_dir, local_dir)

    # 关闭连接
    t.close()
