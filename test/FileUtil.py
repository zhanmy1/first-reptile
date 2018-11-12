# -*- coding: UTF-8 -*-

import conf
import xlwt

config = conf

data_root_path = config.data_root_path

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

#加载数据
def read(resoures_file_path,encode='utf-8'):
    file_path = data_root_path+resoures_file_path
    outputs = []
    for line in open(file_path,encoding=encode):
        if not line.startswith("//"):
            outputs.append(line.strip(','))
    return outputs

#写入数据
def append(resource_file_path,data,encode='utf-8'):
    file_path = data_root_path+resource_file_path
    f = open(file_path,'w+')
    f.truncate()
    f.write(data)
    f.closed

#导入修改次数的表格
def import_count_excel(fields,data):
    #打开一个工作区，可以说就是一个excel文件，不过这个文件在缓存中，没有具体的文件
    exfile = xlwt.Workbook(encoding='utf-8')
    #在这个序列的excel文件中创建一个sheet（页签），后面的cell_overwrite_ok=True是让某一单元格可以重复写入
    sheet = exfile.add_sheet('sheet1',cell_overwrite_ok=True)
    #设置表格中一列的宽度
    sheet.col(0).width = (30 * 567)
    sheet.col(1).width = (30 * 267)

    #生成表头
    """
        我这里将想要的表头内容作为参数放进来了，然后通过enumerate函数处理序列，这样可以获取到序列元素的
    下标和数值，分别是index和value，名字可以自己写，但是顺序是一前一后，然后我们通过这两个数据生成表头
    """
    for index,value in enumerate(fields):
        """
            sheet.write(y,x,value,style)
            write这个函数的参数有四个，最后一个可以没有，y是指的要写入的单元格的行，x是指的要写入的单
        格的列，value就是要写入的值，style就是为这个单元格设置的样式
        """
        #将值写入单元格
        sheet.write(0,index,value,style_head)

    #将传入的数据写入表格
    i = 1
    for item in data:
        sheet.write(i, 0, item[0], style_content)
        sheet.write(i, 1, item[1], style_content)
        i += 1

    #将缓存中的虚拟表格生成为实际的表格
    exfile.save(data_root_path+'data1.xls')

def import_rows_excel(fields,data):
    # 打开一个工作区，可以说就是一个excel文件，不过这个文件在缓存中，没有具体的文件
    exfile = xlwt.Workbook(encoding='utf-8')
    # 在这个序列的excel文件中创建一个sheet（页签）
    sheet = exfile.add_sheet('sheet1',cell_overwrite_ok=True)
    # 设置表格中一列的宽度
    sheet.col(0).width = (30 * 567)
    sheet.col(1).width = (30 * 267)
    sheet.col(2).width = (30 * 267)
    sheet.col(3).width = (30 * 267)

    # 生成表头
    for index,value in enumerate(fields):
        sheet.write(0,index,value,style_head)

    # 将值写入单元格
    i = 1
    for index,item in enumerate(data):
        filename = item[0]
        additions = item[1][0]
        deletions = item[1][1]
        changes = item[1][2]
        sheet.write(i, 0, filename, style_content)
        sheet.write(i, 1, additions, style_content)
        sheet.write(i, 2, deletions, style_content)
        sheet.write(i, 3, changes, style_content)
        i += 1

    # 将缓存中的虚拟表格生成为实际的表格
    exfile.save(data_root_path+'data1.xls')