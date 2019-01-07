# -*- coding: UTF-8 -*-

import GetLocalResult
import datetime
import FileUtil
import conf

def getResult(project,type):
    count_dict = {}
    sord_list = []

    #获取bug-fixing-id，用\n分隔内容，取得所有任务编号的列表
    key_id = FileUtil.read("statistical_data/keyID/"+project+"-"+type+"-keyID.txt").split("\n")
    #生成0.5到0.14.0版本间被删除的文件的在这两版本间的修改记录
    comper_file = FileUtil.read("statistical_data/comper_file.txt").split("\n")
    print(len(comper_file))

    #获取所有文件的提交记录内容格式为：[['编号'，'diff....修改修改']，['编号'，'diff....修改修改]',...]
    results = GetLocalResult.get_all_files(project)
    #遍历获取到的所有文件提交内容
    cont = 0
    for result in reversed(results):
        #reslut[1]为记录结果中的'diff....修改修改'
        content = result[1].splitlines()
        """
           因为在提交记录中存在文件名或文件路径修改的提交数据，但是在逻辑上文件名修改前和修改后的所有提交记录需要统计到一起的，
        所以这里需要将修改前和修改后的文件名取出来进行统计，然后因为data.txt文件中的提交数据是按时间逆序排列的，所以我们最先
        取到的是最新提交的数据，所以要将一个文件的所有历史名字下的所有提交统计到一起，我需要将修改前的名字作为key_name进行获取
        提交内容，将提交后的文件作为文件的现用名作为文件真正的名字（最新的一次提交的提交后名字为最后记录的名字）
        """
        #获取文件名在提交前后的变化，例子：
        #diff --git a/lang/java/avro/src/test/java/org/apache/avro/message/TestBinaryMessageEncoding.java（修改前）
        # b/lang/java/avro/src/test/java/org/apache/avro/message/TestBinaryMessageEncoding.java（修改后）
        s_index = content[0].find('-git a')#截取需要的下标
        e_index = content[0].find(' b')#截取需要的下标

        old_name = content[0][s_index + 6:e_index]#变化前的名字
        new_name = content[0][e_index + 2:len(content[0])]# 变化后的名字

        #设置结果字典中key_name的默认值，setdefault()方法是如果字典中没有key的值，则在字典中插入key，值为后面的参数，如果有
        #就返回已有的值
        """
            设置file_name的默认值，如果没有则返回file_name的值，这个值是从现在到当前节点获取到的所有提交数据,如果文件名发生了
        变化，需要将这个值赋予给新的key_name对应的值，以达到合并的目的
        """
        old_value = count_dict.setdefault(old_name, [ '', 0, 0, 0, 0, 0])

        if comper_file.count(old_name)>0:
            old_value[0] = old_name

        #用获取到的key_id进行筛选
        if key_id.count(result[0]) > 0:
            #遍历文件提交内容，统计其中的+++和---的数量以统计修改行数
            additions = 0
            deletions = 0
            for j,line in enumerate(content):
                if j > 0:
                    if line.startswith('+') and not line.startswith('+++'):
                        additions +=1
                    if line.startswith('-') and not line.startswith('---'):
                        deletions +=1
            old_value[1] += additions
            old_value[2] += deletions
            old_value[3] += additions+deletions
            old_value[4] += 1

        """
            记录文件名的修改，这里没有放到筛选里面是因为，如果文件名的修改被筛选掉了，我们就不能把一个文件的文件名历史完整的
        连起来，这样会导致一个文件的修改记录被断开
        """

        if not old_name == new_name:
            count_dict[new_name] = old_value
            del count_dict[old_name]

    #生成需要的数据
    for item in count_dict.items():
        if item[1][0] != '':
            try:
                item[1][5] = FileUtil.get_file_rows(project,item[0])
            except FileNotFoundError as e:
                sord_list.append(item)

    # 排序
    # sord_list的结构：
    # [('文件名'，['文件名','增加','删除','修改'，'修改次数'，'文件行数'])，('文件名'，
    # ['文件名','增加','删除','修改'，'修改次数'，'文件行数'])，('文件名'，['文件名','增加','删除','修改'，'修改次数'，'文件行数'])]
    sord_compare_list(sord_list)
    return sord_list

#交换序列中两个元素的位置
def swap(li,i, j):
    temp = li[i]
    li[i] = li[j]
    li[j] = temp

#冒泡排序
def sord_compare_list(li):
    length = len(li)
    """
        反向遍历序列li，reversed(range(li))的意思要分开看，range(length)是遍历从0顺序递增到length的所有值，即遍历序列
    [0,1,2,3,4,5......,length]，reversed()是反向遍历序列，所有结果就是遍历序列[length,length-1,.......,2,1,0]
    """
    for i in reversed(range(length)):
        for j in reversed(range(i - 1, length)):
            if li[i][1][4] < li[j][1][4]:
                swap(li,i, j)

if __name__ == '__main__':
    startime = str(datetime.datetime.now())

    fileds = ['文件路径', '总增加行数', '总删除行数', '总修改行数', '修改次数', '总行数']
    data = getResult(conf.now_project, 'New Feature')
    FileUtil.import_compare_excel(fileds, data, conf.now_project, 'New Feature')

    endtime = str(datetime.datetime.now())

    print('开始时间：' + startime)
    print('完成时间：' + endtime)
    #getResult(conf.now_project, conf.type[0])