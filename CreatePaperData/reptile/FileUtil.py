# -*- coding: UTF-8 -*-

import conf
import xlwt
import os
import sys
import xml.etree.ElementTree as ET

config = conf

data_root_path = config.data_root_path
public_path = conf.public_path

#以下是表格的一些样式
#字体
font_head = xlwt.Font()
font_head.bold = True   #加粗

borders = xlwt.Borders()        #单元格的边框
borders.bottom = 1
borders.top = 1
borders.left = 1
borders.right = 1

alignment = xlwt.Alignment()    #单元格内容居中
alignment.horz = xlwt.Alignment.HORZ_CENTER #水平居中
alignment.vert = xlwt.Alignment.VERT_CENTER #垂直居中

#将上面需要的样式放到表头样式中
style_head = xlwt.XFStyle()
style_head.font = font_head
style_head.borders = borders
style_head.alignment = alignment

#将上面需要的样式放到表格内容样式中
style_content = xlwt.XFStyle()
style_content.borders = borders
style_content.alignment = alignment

def check_file_exists(project,file_name):
    path = data_root_path+project+'/'+file_name
    path = path.replace('//','/')
    return os.path.exists(path)

#获取要读取的xml文件
def get_xml_files(filepath):
    filepath = filepath.replace(' ', '')
    file_list = []
    #遍历filepath下所有文件，包括子目录
    files = os.listdir(filepath)
    for fi in files:
            file_list.append(os.path.join(filepath, fi).replace('\\', '/'))
    return file_list

def get_xml_keyID(filepath):
    id_set = set()
    xmlFilePath = os.path.abspath(filepath)
    try:
        tree = ET.parse(xmlFilePath)
        # 获得根节点
        root = tree.getroot()
    except Exception as e:  # 捕获除与程序退出sys.exit()相关之外的所有异常
        print("parse "+ filepath+" fail!")
        sys.exit()

    index = 6
    while (index < len(root[0])):
        id_set.add(root[0][index][5].text)
        index += 1
    # print(len(id_set))
    return id_set

#读取data
def read_data(resoures_file_path,encode='utf-8'):
    file_path = data_root_path+resoures_file_path
    print(file_path)
    return "".join([line for line in open(file_path, encoding=encode)])

#读取文件
def read(resoures_file_path,encode='utf-8'):
    file_path = public_path+resoures_file_path
    file_path = file_path.replace(' ', '')
    return "".join([line for line in open(file_path, encoding=encode)])

#写入数据
def append(prefix,resource_file_path,data,encode='utf-8'):
    file_dir = public_path+prefix
    file_dir = file_dir.replace(' ', '')
    file_path = public_path+prefix+resource_file_path
    file_path = file_path.replace(' ', '')
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = open(file_path,'w+',encoding=encode)
    f.truncate()
    f.write(data)
    f.closed

def get_file_rows(project,file_name):
    path = data_root_path+project+'/'+file_name
    path = path.replace('//','/')
    count = 0
    flag = False
    isFinish = True
    thefile = open(path, 'rb')
    temp = ''
    while True:
        buffer = thefile.read(1024*8192)
        if not buffer:
            break
        if not isFinish:
            count -= 1
        buffer = buffer.decode()
        lines = str(temp+buffer).splitlines()
        if not buffer.endswith('\n'):
            isFinish = False
        for index,value in enumerate(lines):
            value = value.strip()  #除去注释的空格
            if not value=='' and not value.startswith('//'):    #匹配空行
                if value.startswith('/*') and not value.endswith('*/'):
                    flag = True
                elif value.startswith('/*') and value.endswith('*/'):
                    pass
                elif flag == True:
                    if value.endswith('*/'):
                        flag = False
                else:
                    count += 1
    thefile.close()
    return count

def import_local_rows_excel(fileds_one,fileds_two, import_data, project):
    print(fileds_one)
    print(fileds_two)
    # 打开一个工作区，可以说就是一个excel文件，不过这个文件在缓存中，没有具体的文件
    exfile = xlwt.Workbook(encoding='utf-8')
    # 在这个序列的excel文件中创建一个sheet（页签）
    sheet = exfile.add_sheet('sheet1',cell_overwrite_ok=True)
    # 设置表格中一列的宽度
    for i in range(len(fileds_two)+2):
        if i == 0:
            sheet.col(i).width = (10 * 567)
        elif i == 1:
            sheet.col(i).width = (40 * 567)
        else:
            sheet.col(i).width = (30 * 567)

    # 生成表头
    sheet.write_merge(0,1,0,0,fileds_one[0],style_head)
    sheet.write_merge(0,1,1,1,fileds_one[1],style_head)
    sheet.write_merge(0,0,2,len(fileds_two)+1,fileds_one[2],style_head)
    for i in range(len(fileds_two)):
        sheet.write(1, 2+i, fileds_two[i], style_head)
    sheet.write_merge(0, 1, len(fileds_two)+2,len(fileds_two)+2, fileds_one[3], style_head)

    # 将值写入单元格
    index = 2
    for item in import_data.items():
        no = item[0]
        data = item[1]
        #生成编号
        sheet.write_merge(index,index + len(data) -1,0,0,no,style_content)

        #合计
        total = [0 for i in range(len(fileds_two))]
        #生成数据
        for i in range(len(data)):
            for j in range(len(data[i])):
                sheet.write(index + i, 1 + j, data[i][j], style_content)
                if j>0 and j != len(data[i])-1:
                    total[j-1] += data[i][j]
        sheet.write(index + len(data), 0, '合计', style_head)
        sheet.write(index + len(data), 1, len(data), style_head)
        for i in range(len(total)):
            sheet.write(index + len(data), i+2, total[i], style_head)
        sheet.write(index + len(data), len(total)+2, '', style_head)

        index += len(data)+2


    # 将缓存中的虚拟表格生成为实际的表格
    # exfile.save(data_root_path+'data2.xls')
    if not os.path.exists(public_path + 'statistical_data/excel/'+project+'/'):
        os.makedirs(public_path + 'statistical_data/excel/'+project+'/')

    exfile.save(public_path + 'statistical_data/excel/'+project+'/'+project+'-的修改次数.xls')

def import_compare_excel(fields,data,project,type):
    # 打开一个工作区，可以说就是一个excel文件，不过这个文件在缓存中，没有具体的文件
    exfile = xlwt.Workbook(encoding='utf-8')
    # 在这个序列的excel文件中创建一个sheet（页签）
    sheet = exfile.add_sheet('sheet1',cell_overwrite_ok=True)
    # 设置表格中一列的宽度
    sheet.col(0).width = (30 * 567)
    sheet.col(1).width = (30 * 267)
    sheet.col(2).width = (30 * 267)
    sheet.col(3).width = (30 * 267)
    sheet.col(4).width = (30 * 267)
    sheet.col(5).width = (30 * 267)

    # 生成表头
    for index,value in enumerate(fields):
        sheet.write(0,index,value,style_head)

    # 将值写入单元格
    i = 1
    for index,item in enumerate(data):
        filename = item[1][0]
        additions = item[1][1]
        deletions = item[1][2]
        changes = item[1][3]

        sheet.write(i, 0, filename, style_content)
        sheet.write(i, 1, additions, style_content)
        sheet.write(i, 2, deletions, style_content)
        sheet.write(i, 3, changes, style_content)
        sheet.write(i, 4, item[1][4], style_content)
        sheet.write(i, 5, item[1][5], style_content)
        i += 1

    # 将缓存中的虚拟表格生成为实际的表格
    # exfile.save(data_root_path+'data2.xls')
    if not os.path.exists(public_path + 'statistical_data/excel/'):
        os.makedirs(public_path + 'statistical_data/excel/')
    exfile.save(public_path + 'statistical_data/excel/' + project + '中0.5到0.14.0间的修改记录(' + type + ').xls')