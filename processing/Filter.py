import os

import pandas as pd
from pandas import DataFrame
import json
from bson import ObjectId

from database import DatabaseUtil
from model.AnswerRec import AnswerRec
from model.FilterRec import FilterRec
from model.Questionnaire import Questionnaire
from util import FileReader
from util.TimeUtil import to_second
from util.DeleteRecord import DeleteRecord
from util.JsonIO import read_json, write_json


class Filter:
    def __init__(self, data: DataFrame, name="问卷", test=False):
        self.filename = name
        self.source_data = data
        self.result_data = None

        # self.question_count = question_count  # 问题数量
        self.source_rows = data.shape[0]  # 原始行数
        self.result_rows = 0
        self.condition = None
        self.basic_info = None

        self.max_time = None  # 最长时间
        self.min_time = None  # 最短时间
        self.forced_item = None  # 强制项
        self.repeat_item = None  # 重复项
        self.same_percent = None  # 重复相同选项率

        self.idx_col_name = None  # “序号”的实际列名
        self.time_col_name = None  # “测评时间”的实际列名
        self.target_idx = None  # “需要筛选问题”的列号

        self.record = DeleteRecord()
        self.error_rows_record = set()

        # 数据库操作对象
        self.questionnaire_obj = None
        self.answer_recs = list()
        self.filter_rec_obj = None

        self.test = test  # 如果test==False则结果存数据库；否则存为文件到Result

    # 读取并存储“基础信息” Basic.json
    def build_basic_info(self):
        # self.basic_info = json.loads(open("json/Basic.json", 'r', encoding="utf-8").read())
        self.basic_info = read_json("json/Basic.json")
        self.idx_col_name = self.basic_info['IndexColName']  # “序号”的实际列名
        self.time_col_name = self.basic_info['TimeColName']  # “测评时间”的实际列名
        self.target_idx = self.basic_info['TargetColIdx']  # “需要筛选问题”的列号

    # 读取并存储“筛选条件参数” Condition.json
    def build_condition(self):
        # self.condition = json.loads(open("json/Condition.json", 'r').read())
        self.condition = read_json("json/Condition.json")
        self.max_time = self.condition['MaxTime']  # 最长时间
        self.min_time = self.condition['MinTime']  # 最短时间
        self.forced_item = self.condition['ForcedItem']  # 强制项
        self.repeat_item = self.condition['RepeatItem']  # 重复项
        self.same_percent = self.condition['SamePercent']  # 重复相同选项率

    # 开始处理前，先把问卷读取出来
    def get_questionnaire_info(self):
        # 把问题填进去，回答列表声明好，剩下内容待填
        self.questionnaire_obj = Questionnaire(self.source_data.columns.tolist(), [], None, str(ObjectId()),
                                               self.filename)
        return self.questionnaire_obj.questions

    def process(self):
        df = self.source_data

        for index, row in df.iterrows():
            # 由于一条记录可能会出现多种错误，因此先用flag记录，在末尾进行删除
            flag = False  # True表示需要删除，False表示保留

            # 筛选不满足时间要求的
            if to_second(row[self.time_col_name]) > self.max_time:
                self.record.record[0].append(row[self.idx_col_name])
                flag = True
                self.error_rows_record.add(row[self.idx_col_name])
            elif to_second(row[self.time_col_name]) < self.min_time:
                self.record.record[1].append(row[self.idx_col_name])
                flag = True
                self.error_rows_record.add(row[self.idx_col_name])

            # 筛选强制项不正确的
            for forced_i in self.forced_item:
                if str(row[df.columns[forced_i[0]]]) != str(forced_i[1]):
                    self.record.record[2].append(row[self.idx_col_name])
                    flag = True
                    self.error_rows_record.add(row[self.idx_col_name])
                    # 只要有一个强制项不正确就可以结束判断了
                    break

            # 筛选重复项不一样的
            for repeat_i in self.repeat_item:
                if row[df.columns[repeat_i[0]]] != row[df.columns[repeat_i[1]]]:
                    self.record.record[3].append(row[self.idx_col_name])
                    flag = True
                    self.error_rows_record.add(row[self.idx_col_name])
                    # 只要有一对重复题不一致就可以结束判断了
                    break

            # 筛选重复率过高的
            choice_statistics = {}  # 先把每个问题选择的选项统计出来
            question_count = len(self.target_idx)  # 记录问题数量
            for i in self.target_idx:
                choice = row[df.columns[i]]
                if choice in choice_statistics:
                    choice_statistics[choice] = choice_statistics[choice] + 1
                else:
                    choice_statistics[choice] = 1

            choice_percentage = []
            for choice in choice_statistics:  # 然后要统计出每个选项选择的频率
                choice_percentage.append(choice_statistics[choice] / question_count)
            choice_percentage.sort()  # 排序选项出现频率
            if choice_percentage[-1] > self.same_percent:
                self.record.record[4].append(row[self.idx_col_name])
                flag = True
                self.error_rows_record.add(row[self.idx_col_name])

            if flag:
                df = df.drop(index)

        self.result_data = df
        self.result_rows = df.shape[0]

    # 会在存数据库的同时返回信息
    def save_record(self):
        # 将筛选后剩下的回答填入self.questionnaire_obj.answer_rec中
        for index, row in self.result_data.iterrows():
            # 先构建这一条回答的结构
            this_answer = AnswerRec(row[self.idx_col_name], [str(ans) for ans in row.tolist()])
            # 然后插入到问卷的回答列表中
            self.questionnaire_obj.answer_recs.append(this_answer.__dict__)  # 由于要存数据库，所以需要使用__dict__魔法方法

        error_description = [
            ["原始数据行数", str(self.source_rows) + '行'],
            ["有效数据行数", str(self.result_rows) + '行'],
            ["无效数据行数", str(len(self.error_rows_record)) + '行', ','.join(list(map(str, self.error_rows_record)))]
        ]

        df_1 = pd.DataFrame(data=error_description)
        error_type_statistics = []  # 这个是用于输出筛选报告Excel文件的
        error_dic = {}  # 这个是用于存数据库filterRec的
        for i in range(len(self.record.error_type)):
            # error_type_statistics[0].append(str(self.record.error_type[i]) + '行数')
            # error_type_statistics[1].append([str(len(self.record.record[i])) + '行',
            #                                  ','.join(map(str, self.record.record[i]))])
            error_type_statistics.append([str(self.record.error_type[i]) + '行数', str(len(self.record.record[i])) + '行',
                                          ','.join(map(str, self.record.record[i]))])
            error_dic[str(self.record.error_type[i])] = self.record.record[i]
        df_2 = pd.DataFrame(data=error_type_statistics)

        self.filter_rec_obj = FilterRec(self.source_rows, len(self.error_rows_record), error_dic)
        # 最后将这个嵌入questionnaire_obj中，同样需要__dict__魔法方法使其能被数据库解析
        self.questionnaire_obj.filter_rec = self.filter_rec_obj.__dict__

        # 写统计数据文件
        if not os.path.exists(f"Result/{self.filename}/"):
            os.mkdir(f"Result/{self.filename}/")
        with pd.ExcelWriter("Result/" + self.filename + "/" + self.filename + " 数据筛选报告.xlsx") as writer:
            df_1.to_excel(writer, index=False, header=False)
            df_2.to_excel(writer, startrow=4, index=False, header=False)

        # 写原数据文件
        self.source_data.to_excel("Result/" + self.filename + "/" + self.filename + " 原始数据.xlsx", index=False)
        # 写新数据文件
        self.result_data.to_excel("Result/" + self.filename + "/" + self.filename + " 筛选数据.xlsx", index=False)

        # 将结果存数据库
        print(self.questionnaire_obj.__dict__)

        # TEST
        if self.test:
            with open(f'./Result/{self.filename}/{self.filename} 筛选报告.json', 'w', encoding='utf-8') as output_file:
                json.dump(self.questionnaire_obj.__dict__, output_file, ensure_ascii=False)
        else:
            # 由于MongoDB自动添加的ID不能被JSON序列化，因此需要做一步转换，并阻止db自动生成_id
            # obj_dict = {**self.questionnaire_obj.__dict__, '_id': self.questionnaire_obj._id}
            # obj_dict.pop('object_id', None)
            # json_obj = json.dumps(obj_dict, default=DatabaseUtil.default)
            # obj_dict = json.loads(json_obj)
            print(self.questionnaire_obj.__dict__)
            DatabaseUtil.insert(self.questionnaire_obj.__dict__)

        return self.questionnaire_obj.__dict__


if __name__ == '__main__':
    filter = Filter(FileReader.read_source("Source/测试问卷1.xlsx"))
    print(filter.forced_item)
    print(filter.repeat_item)
    print(filter.source_rows)
