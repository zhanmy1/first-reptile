# -*- coding: UTF-8 -*-
#

import GetLocalResult
import GetAPIResult
import datetime
import FileUtil
import conf

def getResult(project):
    count_dict = {}
    results = GetLocalResult.get_all_files(project)
    #遍历获取到的所有文件提交内容
    for result in results:
        old_new_name = GetLocalResult.get_old_new_name(result[1][2])
        old_name = old_new_name[0].replace('//','/')
        new_name = old_new_name[1].replace('//','/')
        #设置结果字典中key_name的默认值，setdefault()方法是如果字典中没有key的值，则在字典中插入key，值为后面的参数，如果有
        #就返回已有的值
        """
            设置old_name的默认值
        """
        old_value = count_dict.setdefault(old_name, [[]for i in range(4)])

        #用获取到的key_id进行筛选
        keyid = result[0]
        if keyid != '':
            old_value[0].append(keyid)
            old_value[1].append(result[1][0])
            old_value[2].append(result[1][1])
            old_value[3].append(int(result[1][0])+int(result[1][1]))
        """
            记录文件名的修改，这里没有放到筛选里面是因为，如果文件名的修改被筛选掉了，我们就不能把一个文件的文件名历史完整的
        连起来，这样会导致一个文件的修改记录被断开
        """
        if not old_name == new_name:
            count_dict[new_name] = old_value
            del count_dict[old_name]
    return count_dict

if __name__ == '__main__':
    startime = str(datetime.datetime.now())

    for project in conf.projects:
        total_data = {}
        fileds_one = ['编号', '文件路径', '类型','文件行数']
        fileds_two = []
        for type in conf.type:
            fileds_two.append(type)
            newfeature_id_list = FileUtil.read("statistical_data/keyID/"+project+"-NewFeature-keyID.txt").split("\n")
            type_id_list = []
            if type=='Change':
                type_id_list = None
            else:
                print('当前读取' + project + '的' + type + '的keyID数据')
                type_id_list = FileUtil.read("statistical_data/keyID/" + project + "-" + type + "-keyID.txt").split("\n")
            result = getResult(project)

            for item in result.items():
                file_name = item[0]
                if FileUtil.check_file_exists(project, file_name) and (file_name.endswith(".java") or file_name.endswith(".java.t"))\
                        and not file_name.count('/src/test'):
                    ary = GetAPIResult.total_array(item[1],newfeature_id_list,type_id_list)
                    print(ary)
                    if ary[0] != '':
                        old_value = total_data.setdefault((ary[0],file_name),[])
                        old_value.append(ary[4])

        import_data = {}
        for item in total_data.items():
            file_name = item[0][1]
            item[1].insert(0,file_name)
            old_value = import_data.setdefault(item[0][0],[])
            old_value.append(item[1])

        for item in import_data.items():
            for data in item[1]:
                data.append(FileUtil.get_file_rows(project,data[0]))
        #生成excel
        FileUtil.import_local_rows_excel(fileds_one,fileds_two, import_data, project)

    endtime = str(datetime.datetime.now())

    print('开始时间：' + startime)
    print('完成时间：' + endtime)
    #getResult(conf.now_project, conf.type[0])