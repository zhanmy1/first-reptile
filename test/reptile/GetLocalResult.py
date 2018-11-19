# -*- coding: UTF-8 -*-

import FileUtil
import os

def get_all_files():
    all_files = []

    data = FileUtil.read('data.txt')
    commits = data.split('commit ')
    for i,commit in enumerate(commits):
        files = commit.split('diff -')
        del files[0]
        all_files.extend(files)

    return all_files

def get_need_files(filepath):
    file_list = []
    #遍历filepath下所有文件，包括子目录
    files = os.listdir(filepath)
    for fi in files:
        if fi == '.git':
            continue
        fi_d = os.path.join(filepath,fi)
        if os.path.isdir(fi_d):
            get_need_files(fi_d)
        else:
            if fi_d.endswith('.java'):
                file_list.append(os.path.join(filepath, fi_d).replace('\\', '/'))
    return file_list