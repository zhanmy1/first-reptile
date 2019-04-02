# -*- coding: UTF-8 -*-

import random

#系统操作目录，几个库文件的Data放这里
data_root_path = 'D:/sublime/'

#公共目录,生成的excel和keyID放这里
public_path = 'D:/sublime/'

#在jira上查询的项目名
# projects = ['AURORA','AVRO','FLINK','FLUME','HIVE','MAHOUT','STORM']
type = ['New Feature','Change']
projects = ['FLINK','FLUME','HIVE','STORM','FOP','JCLOUDS','MANIFOLDCF','SHINDIG','HBASE','CAMEL']
# projects = ['HBASE']
# type = ['Bug','New Feature']

#当前要为谁生成excel
now_project = 'MAHOUT'
version = ''

#用于匹配编号的正则表达式
match = {
    'FLINK':'[Ff][Ll][Ii][Nn][Kk][-_]\d+',
    'FLUME':'[Ff][Ll][Uu][Mm][Ee][-_]\d+',
    'HIVE':'[Hh][Ii][Vv][Ee][-_]\d+',
    'STORM':'[Ss][Tt][Oo][Rr][Mm][-_]\d+',
    'FOP':'[Ff][Oo][Pp][-_]\d+',
    'JCLOUDS':'[Jj][Cc][Ll][Oo][Uu][Dd][Ss][-_]\d+',
    'MANIFOLDCF':'[Cc][Oo][Nn][Nn][Ee][Cc][Tt][Oo][Rr][Ss][-_]\d+',
    'SHINDIG':'[Ss][Hh][Ii][Nn][Dd][Ii][Gg][-_]\d+',
    'CAMEL':'[Cc][Aa][Mm][Ee][Ll][-_]\d+',
    'HBASE':'[Hh][Bb][Aa][Ss][Ee][-_]\d+'
}

#浏览器型号参数
user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]

#爬虫的请求头
headers = {'User-Agent': random.choice(user_agent_list),
           'Content-Type': 'application/json',
           'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'cookie': 'seraph.rememberme.cookie=370152%3Af7da1d0ac59c32b59e6fd5ab5d27f735dea7d6cc; JSESSIONID=B9E612A1803C5C25DB69BDD824EE2B6E; atlassian.xsrf.token=A5KQ-2QAV-T4JA-FDED|dd52fae16b19767ae0dc8e786c8dd51cbe7e5091|lout'
           }