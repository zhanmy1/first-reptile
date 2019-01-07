# -*- coding: UTF-8 -*-

import random

#系统操作目录
data_root_path = 'D:/sublime/'

#公共目录
public_path = 'F:/Desktop/导师任务/数据/'

#在jira上查询的项目名
projects = ['MAHOUT','AVRO','AURORA','FLINK','FLUME','STORM']
type = ['Bug','Improvement','New Feature']

#当前要为谁生成excel

version = ''
start_commitID = ''
end_commitID = '1292145799e70890d4898353e4f5279d0484c5b7'

#用于匹配编号的正则表达式
match = {
    'MAHOUT':'[Mm][Aa][Hh][Oo][Uu][Tt][-_]\d*',
    'AVRO':'[Aa][Vv][Rr][Oo][-_]\d*',
    'AURORA':'[Aa][Uu][Rr][Oo][Rr][Aa][-_]\d*',
    'FLINK':'[Ff][Ll][Ii][Nn][Kk][-_]\d*',
    'FLUME':'[Ff][Ll][Uu][Mm][Ee][-_]\d*',
    'STORM':'[Ss][Tt][Oo][Rr][Mm][-_]\d*'
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
           'cookie': 'seraph.rememberme.cookie=357534%3A2c146a18cc241e6231ac0974da0fd83842b84600; JSESSIONID=14C103F53DF1413AD3FC3A0B8FE26C04; atlassian.xsrf.token=A5KQ-2QAV-T4JA-FDED|aa21d726d4eb494d41df047a12cc487dbb8fe533|lin'
           }