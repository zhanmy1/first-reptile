# -*- coding: UTF-8 -*-

import FileUtil
import conf

if __name__ == '__main__':
    #获取所有的bug文件
    files = FileUtil.get_xml_files(conf.public_path+"avro-jira-bugs")

    #遍历bug文件，解析其中的xml数据并将数据写到一个文本文件中
    #用集合set进行统计，方便去重
    id_set = set()
    for file in files:
        #将所有的获取的keyID的集合合并，取并集
        id_set = id_set | FileUtil.get_xml_keyID(file)
    FileUtil.append("statistical_data/","keyID.txt","\n".join(id_set))