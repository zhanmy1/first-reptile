# -*- coding: UTF-8 -*-

import MainUtil
import datetime
import conf
import ResultUtil

def getResult():
    page = 1
    per_page = 100
    #获取所有的提交记录
    commits = ResultUtil.get_all_commits(page,per_page)

    cont_dict = {}
    sort_li = []
    i = 0
    for item in commits:
        #获取某一次提交记录
        i += 1
        files_result = ResultUtil.get_commits_files(conf.headers,item['sha'])
        if files_result==None:
            continue
        print(i,files_result['files'])

        #遍历这次提交记录中的files数据
        for item_file in files_result['files']:
            file_name = item_file['filename']
            """
                setdefault函数是给字典中某一key设置value，如果这个key不存在就设置后面的value，如果存在就返回已存
            在的值，所以如果某一key（文件名）已经在字典里面，那么直接对这个key对应的value（修改次数）加一
            即可，如果不存在，就设置这个新的key（文件名）的value（修改次数）为0，然后因为是第一次获取到，就直接
            再0之上加一即可
            """
            cont_dict.setdefault(file_name,0)
            cont_dict[file_name] += 1

    for item in cont_dict.items():
        sort_li.append(item)
    #递减排序
    sort_li.sort(key=lambda x:(-x[1],x[0]))

    return sort_li


if __name__ == '__main__':
    print('开始时间：'+str(datetime.datetime.now()))

    MainUtil.do()

    print('完成时间：'+str(datetime.datetime.now()))