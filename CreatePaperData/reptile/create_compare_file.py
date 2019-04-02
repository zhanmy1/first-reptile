# -*- coding: UTF-8 -*-

import datetime
import conf
import os
import FileUtil

def getResult(file_dir):
   compare_file = []
   for root, dirs, files in os.walk(file_dir):
       for file in files:
            file_path = os.path.join(root, file)
            file_path = file_path.replace('\\','/')
            file_path = file_path.replace(conf.data_root_path+conf.now_project,'')
            if file_path.endswith('.java') or file_path.endswith('.java.t'):
                rows = FileUtil.get_file_rows(conf.now_project, file_path)
                compare_file.append(str(file_path)+','+str(rows))
   FileUtil.append("statistical_data/", "comper_file.txt", "\n".join(compare_file))

if __name__ == '__main__':
    startime = str(datetime.datetime.now())

    getResult(conf.data_root_path+conf.now_project)

    endtime = str(datetime.datetime.now())

    print('开始时间：' + startime)
    print('完成时间：' + endtime)