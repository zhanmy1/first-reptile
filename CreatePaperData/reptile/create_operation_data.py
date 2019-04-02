# -*- coding: UTF-8 -*-

import FileUtil
import re
import conf

def get_all_files(project):
    #获取用diff -分隔出来的所有提交文件
    all_files = []

    # data = FileUtil.get_commit_data('data.txt')
    # commits = data.split('truecommit')
    #用\ncommit进行分隔，因为真正的提交标识都是从一行的最开始出现的
    commits = FileUtil.read_data('DATAS'+'/DATA-'+project+'.txt').split('\ncommit')
    flag = True
    if conf.start_commitID == '' and conf.end_commitID != '':
        flag = False
    for commit in commits:
        files = commit.split('\ndiff -')
        heads = files[0].splitlines()
        head = heads[4].lstrip()
        commitID = heads[0].lstrip()

        if conf.start_commitID == '' and conf.end_commitID == '':
            flag = False
        elif  commitID == conf.start_commitID:
            flag = False

        if flag:
            continue
        no = ''
        suited = re.match(conf.match,head)
        if suited:
            no = suited.group(0)
        all_files.extend(files)

        if commitID == conf.end_commitID:
            break
    return all_files