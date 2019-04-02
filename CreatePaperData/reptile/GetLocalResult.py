# -*- coding: UTF-8 -*-

import FileUtil
import re
import conf

def get_all_files(project):
    #获取用diff -分隔出来的所有提交文件
    all_files = []
    #用\ncommit进行分隔，因为真正的提交标识都是从一行的最开始出现的
    commits = FileUtil.read_data('DATAS'+'/DATA-'+project+'.txt').split('\ncommit')
    for commit in commits:
        content = commit.splitlines()
        no = ''
        #使用正则表达式进行匹配
        """
            re是python中使用正则表达式的包，match方法是从传入的字符串的开始进行匹配，返回的值为一个特殊格式的字符串，
        （例子：<re.Match object; span=(0, 6), match='AVRO-9'>），span是匹配字符串的下标，可以用span()方法获取，
        match是匹配的内容，可以用group()方法获取，如果没有匹配则返回none(none在if后面表示false,个人感觉)
        """
        for i,line in enumerate(content):
            if i==4:
                suited = re.search(conf.match[project], line)
                if suited:
                    no = suited.group()
            elif i>4:
                if re.match('\d+\t\d+\t',line):
                    change = line.split('\t')
                    all_files.append([no,change])
    return all_files

def get_old_new_name(file_name):
    temp = file_name
    old_name = file_name
    new_name = file_name
    while True:
        suited = re.search('\{.+=>.+\}',temp)
        if suited:
            file_change = suited.group()
            file_change = file_change[1:len(file_change)-1]
            file_change_bf = file_change.split(' => ')
            old_name = re.sub('\{.+=>.+\}',file_change_bf[0],old_name,1)
            new_name = re.sub('\{.+=>.+\}', file_change_bf[1], new_name, 1)
            temp = re.sub('\{.+=>.+\}', '', temp, 1)
        else:
            if temp.count('=>'):
                temps = temp.split('=>')
                temp = temp.replace('=>','')
                old_name = temps[0]
                new_name = temps[1]
            else:
                break
    return (old_name,new_name)
