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

    for commit in commits:
        files = commit.split('\ndiff -')
        heads = files[0].splitlines()

        no = ''
        #使用正则表达式进行匹配
        """
            re是python中使用正则表达式的包，match方法是从传入的字符串的开始进行匹配，返回的值为一个特殊格式的字符串，
        （例子：<re.Match object; span=(0, 6), match='AVRO-9'>），span是匹配字符串的下标，可以用span()方法获取，
        match是匹配的内容，可以用group()方法获取，如果没有匹配则返回none(none在if后面表示false,个人感觉)
        """
        for head in heads:
            suited = re.search(conf.match[project], head)
            if suited:
                no = suited.group(0)
                break
        change_files(files,no)
        all_files.extend(files)

    return all_files

def change_files(files,no):
    del files[0]
    for i,file in enumerate(files):
        files[i] = [no.upper(),file]