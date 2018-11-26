# -*- coding: UTF-8 -*-
import re

import FileUtil
import os

def get_all_files():
    all_files = []

    data = FileUtil.read('data.txt')
    commits = data.split('truecommit')
    for i,commit in enumerate(commits):
        if i==0:
            continue
        files = commit.split('diff -')
        heads = files[0].splitlines()
        head = heads[4].lstrip()  #去除空格
        no = ''
        if re.match('[Aa][Vv][Rr][Oo][-_]',head):
            index = head.find(' ')
            no = head[:index]
            print(no)
        change_files(files,no)
        all_files.extend(files)
    return all_files

def change_files(files,no):
    del files[0]
    for i,file in enumerate(files):
        files[i] = [no,file]

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