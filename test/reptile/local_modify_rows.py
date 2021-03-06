# -*- coding: UTF-8 -*-
#

import GetLocalResult
import GetAPIResult
import Main
import datetime
import FileUtil
import conf

def getResult(project,type):
    count_dict = {}
    sord_list = []

    #获取bug-fixing-id，用\n分隔内容，取得所有任务编号的列表
    print('当前读取' + project + '的' + type + '的keyID数据')
    key_id = FileUtil.read("statistical_data/keyID/"+project+"-"+type+"-keyID.txt").split("\n")
    print(len(key_id))
    #获取所有文件的提交记录内容格式为：[['编号'，'diff....修改修改']，['编号'，'diff....修改修改]',...]
    results = GetLocalResult.get_all_files(project)
    #遍历获取到的所有文件提交内容
    cont = 0
    #reversed是反向遍历序列，这样可以从最开始的提交进行统计
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
            设置old_name的默认值
        """
        old_value = count_dict.setdefault(old_name, [ 0, 0, 0, 0, 0])

        #用获取到的key_id进行筛选
        #if key_id.count(result[0]) > 0:
        #遍历文件提交内容，统计其中的+++和---的数量以统计修改行数
        if result[0] != '' and key_id.count(result[0]):
            additions = 0
            deletions = 0
            for j,line in enumerate(content):
                if j > 0:
                    if line.startswith('+') and not line.startswith('+++'):
                        additions +=1
                    if line.startswith('-') and not line.startswith('---'):
                        deletions +=1
            old_value[0] += additions           #增加行数
            old_value[1] += deletions           #删除行数
            old_value[2] += additions+deletions #修改行数
            old_value[3] += 1                   #修改次数

            if content[1].startswith('new file'):
                old_value[6] += 1
            elif content[1].startswith('deleted file'):
                old_value[7] += 1
            else:
                old_value[5] += 1

        """
            记录文件名的修改，这里没有放到筛选里面是因为，如果文件名的修改被筛选掉了，我们就不能把一个文件的文件名历史完整的
        连起来，这样会导致一个文件的修改记录被断开
        """
        if not old_name == new_name:
            count_dict[new_name] = old_value
            del count_dict[old_name]

    #筛选java文件，并记录java文件的行数（忽略注释行数）
    for item in count_dict.items():
        """
            这里是过滤是否显示的地方，现在是显示所有的java文件记录，你看看结果会发现有很多记录是全是0的，是因为它们所有的提交
            记录全被keyID过滤了，只剩下文件名显示出来了，所以你可以看情况把这些都删掉，就是在这个判断条件后面加上一个
             and item[0][3] != 0
        """
        if (item[0].endswith(".java") or item[0].endswith(".java.t")):
            try:
                item[1][4] = FileUtil.get_file_rows(project,item[0])
            except FileNotFoundError as e:
                """
                    这里是异常处理，如果文件被删了，就不对文件行数处理，就为默认值0，如果你想把这些被删除的文件也处理掉，就
                    把pass改成continue
                """
                pass
            sord_list.append(item)
    # 排序
    # sord_list的结构：
    # [('文件名'，['文件名','增加','删除','修改'，'修改次数'，'文件行数'])，('文件名'，
    # ['文件名','增加','删除','修改'，'修改次数'，'文件行数'])，('文件名'，['文件名','增加','删除','修改'，'修改次数'，'文件行数'])]
    GetAPIResult.sord_list(sord_list)
    return sord_list

if __name__ == '__main__':
    startime = str(datetime.datetime.now())

    Main.do()

    endtime = str(datetime.datetime.now())

    print('开始时间：' + startime)
    print('完成时间：' + endtime)
    #getResult(conf.now_project, conf.type[0])