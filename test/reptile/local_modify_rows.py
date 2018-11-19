# -*- coding: UTF-8 -*-

import GetLocalResult
import GetAPIResult
import Main
import datetime

def getResult():
    count_dict = {}
    sord_list = []

    files = GetLocalResult.get_all_files();

    for i,file in enumerate(files):
        if i == 0:
            continue
        additions = 0
        deletions = 0
        file_name = ''
        key_name = ''
        content = file.split('\n')
        for j,line in enumerate(content):
            if j == 0:
                s_index = line.find('-git a')
                e_index = line.find(' b')
                key_name = line[s_index+6:e_index]
                file_name = line[e_index + 2:len(line)]
            else:
                if line.startswith('+') and not line.startswith('+++'):
                    additions +=1
                if line.startswith('-') and not line.startswith('---'):
                    deletions +=1
        count_dict.setdefault(key_name, [file_name,0, 0, 0])
        old_value = count_dict.setdefault(file_name, [file_name,0, 0, 0])
        old_value[1] += additions
        old_value[2] += deletions
        old_value[3] += additions+deletions
        if not key_name == file_name:
            count_dict[key_name] = old_value
            del count_dict[file_name]

    for item in count_dict.items():
        if item[1][0].endswith('java'):
            sord_list.append(item)
        # 排序
        # sord_list的结构：
        # [('文件名'，['文件名','增加','删除','修改'])，('文件名'，['文件名','增加','删除','修改'])，('文件名'，['文件名','增加','删除','修改'])]
    GetAPIResult.sord_list(sord_list)

    return sord_list

if __name__ == '__main__':
    print('开始时间：' + str(datetime.datetime.now()))

    Main.do()

    print('完成时间：' + str(datetime.datetime.now()))