# -*- coding: UTF-8 -*-

import FileUtil
import conf
import GetAPIResult
import arrow
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.cElementTree as ET

def get_data(interval):
    #获取月份区间
    """
        arrow.now()是获取当前的时间，shift()方法相当于一个游标，它指着一个时间线，设置mongth的值可以将时间往以前的时间移动，并
    返回时间数值，然后用format方法设置返回的格式，YYYY-MM-1即获取时间的年月加上第一天的日期
    """
    start_m = arrow.now().shift(months=-interval).format("YYYY-MM-1")
    end_m = arrow.now().shift(months=-interval+1).format("YYYY-MM-1")#参数加1即时间往现在推一个月，时间间隔则为一个月
    result = GetAPIResult.get_month_data(conf.headers,start_m,end_m)
    #处理获取到的数据的xml数据字符串
    root = ET.fromstring(result)
    #total为本次查询结果的report数量
    total = int(root[0][4].attrib['total'])
    #当有report数据的时候才生成xml文件
    if(total>0):
        FileUtil.append("/avro-jira-bugs/",conf.project.upper()+start_m+"-"+end_m+".xml",result)
    #返回这一次获取的report数量，用来统计以查询出的report数量
    return total

if __name__ == '__main__':
    #获取所有report的总数
    all_data = GetAPIResult.get_all_data(conf.headers)
    #ET.formstring可以像处理xml文件一样处理xml格式的字符串，返回一个树结构
    all_root = ET.fromstring(all_data)
    #观察返回的树结构，我可以知道，total的值在all_root[0][4].attrib['total']的位置
    all_total = int(all_root[0][4].attrib['total'])
    print(all_total)
    #统计已经查询出的report数量
    now_total = 0
    #调整查询的月份
    interval = 0
    while True:
        #输出已查询出的reprot数量
        print(now_total)
        #统计
        now_total += int(get_data(interval))
        #当已查询出的reprot数量等于总数量时退出查询
        if now_total >= all_total:
            break
        interval += 1