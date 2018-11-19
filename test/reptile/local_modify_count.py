# -*- coding: UTF-8 -*-

import GetLocalResult
import Main
import datetime
import FileUtil

def getResult():
    count_dict = {}
    sort_li = []

    files = GetLocalResult.get_all_files();

    for i, file in enumerate(files):
        if i == 0:
            continue
        content = file.split('\n')
        line = content[0]
        s_index = line.find('-git a')
        e_index = line.find(' b')
        file_name = line[e_index + 3:len(line)]
        key_name = line[s_index + 7:e_index]


        count_dict.setdefault(key_name, [file_name,0, 0])
        old_value = count_dict.setdefault(file_name, [file_name,0, 0])
        if not file_name == key_name:
            count_dict[key_name] = old_value
            del count_dict[file_name]

        count_dict[key_name][1] += 1

    for item in count_dict.items():
        if item[1][0].endswith('.java'):
            try:
                item[1][2] = FileUtil.get_file_rows(item[1][0])
            except FileNotFoundError as e:
                item[1][2] = 0
            sort_li.append(item)
        # 递减排序
    sort_li.sort(key=lambda x: (-x[1][1], x[1][0]))

    return sort_li

if __name__ == '__main__':
    print('开始时间：' + str(datetime.datetime.now()))

    Main.do()

    print('完成时间：' + str(datetime.datetime.now()))