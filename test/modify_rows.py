# -*- coding: UTF-8 -*-

import conf
import ResultUtil
import MainUtil
import datetime

def getResult():
    page = 1
    per_page = 100
    #获取所有的提交记录
    commits = ResultUtil.get_all_commits(page,per_page)

    cont_dict = {}
    sord_list = []

    i = 0
    for item in commits:
        #查询某一次提交
        i+=1
        files_result = ResultUtil.get_commits_files(conf.headers,item['sha'])
        #遍历获取的files数据
        if files_result==None:
            continue
        print(i,files_result['files'])
        for item_file in files_result['files']:
            filename = item_file['filename']
            additions = item_file['additions']
            deletions = item_file['deletions']
            changes = item_file['changes']

            cont_dict.setdefault(filename,[0,0,0])
            cont_dict[filename][0] += additions
            cont_dict[filename][1] += deletions
            cont_dict[filename][2] += changes

    for item in cont_dict.items():
        sord_list.append(item)
    #排序
    ResultUtil.sord_list(sord_list)

    return sord_list


if __name__ == '__main__':
    print('开始时间：' + str(datetime.datetime.now()))

    MainUtil.do()

    print('完成时间：' + str(datetime.datetime.now()))