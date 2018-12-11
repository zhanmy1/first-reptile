# -*- coding: UTF-8 -*-

import FileUtil
import conf
import GetAPIResult
import arrow
import xml.sax
import xml.sax.handler

#不是很懂，只能懂大概。。。应该是重写了ContentHandler里的几个方法，parseString会调用这几个方法
class XMLHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.buffer = ""
        self.mapping = {}

    def startElement(self, name, attributes):
        self.buffer = ""

    def characters(self, data):
        self.buffer += data

    def endElement(self, name):
        self.mapping[name] = self.buffer

    def getDict(self):
        return self.mapping

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
    xh = XMLHandler()
    xml.sax.parseString(result, xh)
    ret = xh.getDict()
    #通过测试知道，当没有提交数据的时候，返回的ret的长度为11，所有通过递归，一直查询到ret的长度为11即可
    if(len(ret)>11):
        FileUtil.append("/avro-jira-bugs/AVRO_"+start_m+"-"+end_m+".xml",result)
        get_data(interval+1)

if __name__ == '__main__':
    get_data(0)