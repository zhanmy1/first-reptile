# -*- coding: UTF-8 -*-
#处理爬虫请求与排序的模块

from urllib.request import Request
from urllib.request import urlopen
from urllib.request import ProxyHandler
from urllib.request import build_opener
from urllib.request import install_opener
import requests

proxy_info = {'host': 'web-proxy.oa.com', 'port': 8080}
proxy_support = ProxyHandler({"http": "http://%(host)s:%(port)d" % proxy_info})
opener = build_opener(proxy_support)
install_opener(opener)

#用爬虫获取bug管理系统中一个月的任务提交数据
#headers为请求头，start_m为开始的月份，end_m为结束的月份
def get_month_data(headers,start_m,end_m):
    #请求的地址
    url = 'https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?' \
          'jqlQuery=project+%3D+AVRO+AND+issuetype+%3D+Bug+AND+created+%3E' \
          '%3D+{start_m}+AND+created+%3C%3D+{end_m}+' \
          'ORDER+BY+priority+DESC%2C+updated+DESC&tempMax=1000'.format(start_m=start_m, end_m=end_m)
    #打印地址便于差错
    print(url)
    #爬虫向目标地址发出请求
    # req = Request(url, headers=headers)
    # #获取目标地址的回复内容
    # response = urlopen(req).read()
    # #response为字节码(01000010001这种)，通过decode()方法可将字节码转换为字符串
    #
    # result = response.decode()
    # #返回地址回复的内容
    session = requests.Session()
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
            if li[i][1][4] < li[j][1][4]:
                swap(li,i, j)