# -*- coding: UTF-8 -*-

import FileUtil
import local_modify_rows

def do():
    # 生成文件修改行数记录表-----Local
    fileds = ['文件路径','总增加行数','总删除行数','总修改行数','修改次数','总行数']
    FileUtil.import_local_rows_excel(fileds, local_modify_rows.getResult())
