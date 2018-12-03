import xml.etree.ElementTree as ET
import os
import sys
import conf

def traverseXml(element,i):
    #print (len(element))
    if len(element)>0:
        for child in element:
            print (i*"\t"+child.tag, "----", child.attrib)
            traverseXml(child,i+1)
    #else:
        #print (element.tag, "----", element.attrib)


if __name__ == "__main__":
    #将输入的路径转换为可识别的路径
    xmlFilePath = os.path.abspath(conf.data_root_path+"/avro-jira-bugs/AVRO_2009-4-1_2009-5-1.xml")
    try:
        #将xml文件转换为树结构，一层一层的
        tree = ET.parse(xmlFilePath)

        # 获得根节点，root
        root = tree.getroot()
    except Exception as e:  # 捕获除与程序退出sys.exit()相关之外的所有异常
        print("parse AVRO_2009-4-1_2009-5-1.xml fail!")
        sys.exit()
    #查看根节点的一些信息，tag是节点名字，attrib是节点的属性列表
    print(root.tag, "----", root.attrib)

    # 遍历root的下一层
    for child in root:
        print("遍历root的下一层", child.tag, "----", child.attrib)
    print(20 * "*")

    # 遍历xml文件
    traverseXml(root,0)
    print(20 * "*")

    index = 6
    while (index < len(root[0])):
        print(root[0][index][7].tag + "-------" + root[0][index][7].text)    #tag标签的名字，text标签的内容
        print(root[0][index][5].tag + "-------" + root[0][index][5].text)
        index += 1
    print(20 * "*")


    # 根据标签名查找root下的所有标签
    # captionList = root.findall("item")  # 在当前指定目录下遍历
    # print(len(captionList))
    # for caption in captionList:
    #     print(caption.tag, "----", caption.attrib, "----", caption.text)