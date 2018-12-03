# -*- coding: UTF-8 -*-

from urllib.request import Request
from urllib.request import urlopen
from urllib.request import ProxyHandler
from urllib.request import build_opener
from urllib.request import install_opener
import json
import conf

proxy_info = {'host': 'web-proxy.oa.com', 'port': 8080}
proxy_support = ProxyHandler({"http": "http://%(host)s:%(port)d" % proxy_info})
opener = build_opener(proxy_support)
install_opener(opener)


#获取一页的提交记录
def get_page_commits(headers,page,per_page):
    url = 'https://api.github.com/repos/{rep}/commits?page={page}&per_page={per_page}'.format(rep=conf.rep,page=page,per_page=per_page)

    req = Request(url, headers=headers)
    response = urlopen(req).read()
    result = json.loads(response.decode())

    print(page)

    return result

#获取所有的提交记录，page为记录的开始页数，per_page是一页记录数，一页的记录数越少请求的频率越高
def get_all_commits(page,per_page):
    commits = []

    while True:
        #调用获取一页记录数的函数
        results = get_page_commits(conf.headers,page,per_page)
        #将获取的记录数储存起来
        """" 因为到最后一页的时候，记录数会小于一页数所有对
        查询出的记录数进行判断可以判断是否查询到最后一页 """
        if len(results)==per_page:
            page += 1

            for item in results:
                commits.append(item)
        else:
            for item in results:
                commits.append(item)
            break

    return commits

"""
    由于查询出的commit的数据中没有具体的提交文件的信息，但是我对某一次提交进行查询的
时候发现返回的数据中有files的信息，所有用下面这个方法查询某一具体的提交记录
"""
#查询某一具体提交记录
def get_commits_files(headers,sha):
    url = 'https://api.github.com/repos/{rep}/commits/{sha}'.format(rep=conf.rep,sha=sha)

    print(url)

    req = Request(url, headers=headers)
    response = urlopen(req).read()
    result = json.loads(response.decode())
    return result

#将元组转换为固定格式的字符串
def change_cont_tuple(tuple):
    return str(tuple[0])+'-------------------------->'+str(tuple[1])

#将元组转换为固定格式的字符串
def change_rows_tuple(tuple):
    filename = str(tuple[0])
    additions = str(tuple[1][0])
    deletions = str(tuple[1][1])
    changes = str(tuple[1][2])

    return filename+'\n'+'总增加行数：'+additions+'\t'+'总删除行数：'+deletions+'\t'+'总共修改行数：'+changes

#交换序列中两个元素的位置
def swap(li,i, j):
    temp = li[i]
    li[i] = li[j]
    li[j] = temp

#冒泡排序
def sord_list(li):
    length = len(li)
    for i in reversed(range(length)):#反向遍历序列reversed(range(li))
        for j in reversed(range(i - 1, length)):
            if li[i][1][4] < li[j][1][4]:
                swap(li,i, j)