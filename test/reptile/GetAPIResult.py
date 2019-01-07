# -*- coding: UTF-8 -*-
#处理爬虫请求与排序的模块

from urllib.request import Request
from urllib.request import urlopen
from urllib.request import ProxyHandler
from urllib.request import build_opener
from urllib.request import install_opener
import requests
import conf

proxy_info = {'host': 'web-proxy.oa.com', 'port': 8080}
proxy_support = ProxyHandler({"http": "http://%(host)s:%(port)d" % proxy_info})
opener = build_opener(proxy_support)
install_opener(opener)

#用爬虫获取bug管理系统中一个月的任务report数据
#headers为请求头，start_m为开始的月份，end_m为结束的月份
def get_month_data(headers,start_m,end_m,project,type):
    if type.find(' ') > 0:
        type = type.replace(' ', '+')
        type = "\"" + type + "\""
    session = requests.Session()
    #请求的地址
    url = 'https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?' \
      'jqlQuery=project+%3D+{project}+AND+issuetype+%3D+{type}+AND+created+%3E' \
      '%3D+{start_m}+AND+created+%3C%3D+{end_m}+' \
      'ORDER+BY+priority+DESC%2C+updated+DESC&tempMax=1000'.format(project=project,type=type,start_m=start_m, end_m=end_m)
    #打印地址便于查错
    print(str(url))
    result = ''
    #利用会话进行请求，一个会话可以进行多次请求
    try:
        req = session.get(url,headers=headers,proxies=proxy_info,timeout=10)
        result = req.text
    except requests.exceptions.Timeout:
        print('请求超时，重试请求')
        result = get_month_data(headers, start_m, end_m,project,type)
    except Exception:
        result = get_month_data(headers,start_m,end_m,project,type)
    #返回网页内容的字符串
    return result

#用爬虫查询所有的report数据，不需要具体数据，只需要总数量即可，所以在url中将tempMax设置为0
def get_all_data(headers,project,type):
    if type.find(' ') > 0:
        type = type.replace(' ', '+')
        type = "\"" + type + "\""
    session = requests.Session()
    # 请求的地址
    url = 'https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?' \
          'jqlQuery=project+%3D+{project}+AND+issuetype+%3D+{type}+' \
          '&tempMax=0'.format(project=project,type=type)
    # 打印地址便于查错
    print(url)
    req = session.get(url, headers=headers, proxies=proxy_info)
    return req.text

#交换序列中两个元素的位置
def swap(li,i, j):
    temp = li[i]
    li[i] = li[j]
    li[j] = temp

#冒泡排序
def sord_list(li):
    length = len(li)
    """
        反向遍历序列li，reversed(range(li))的意思要分开看，range(length)是遍历从0顺序递增到length的所有值，即遍历序列
    [0,1,2,3,4,5......,length]，reversed()是反向遍历序列，所有结果就是遍历序列[length,length-1,.......,2,1,0]
    """
    for i in reversed(range(length)):
        for j in reversed(range(i - 1, length)):
            if li[i][1][3] < li[j][1][3]:
                swap(li,i, j)