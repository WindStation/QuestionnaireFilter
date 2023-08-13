import pandas as pd
from pandas import DataFrame
import json
import FileReader
from TimeUtil import to_second
from DeleteRecord import DeleteRecord


class Filter:
    def __init__(self, data: DataFrame, question_count: int, name="问卷"):
        self.filename = name
        self.source_data = data
        self.result_data = None

        self.question_count = question_count  # 问题数量
        self.source_rows = data.shape[0]  # 原始行数
        self.result_rows = 0
        self.condition = json.loads(open("json/Condition.json", 'r').read())

        self.max_time = self.condition['MaxTime']  # 最长时间
        self.min_time = self.condition['MinTime']  # 最短时间
        self.forced_item = self.condition['ForcedItem']  # 强制项
        self.repeat_item = self.condition['RepeatItem']  # 重复项
        self.same_percent = self.condition['SamePercent']  # 重复相同选项率

        self.record = DeleteRecord()
        self.error_rows_record = set()

    def process(self):
        df = self.source_data

        for index, row in df.iterrows():
            # 由于一条记录可能会出现多种错误，因此先用flag记录，在末尾进行删除
            flag = False  # True表示需要删除，False表示保留

            # 筛选不满足时间要求的
            if to_second(row['测评时长']) > self.max_time:
                self.record.record[0].append(index)
                flag = True
                self.error_rows_record.add(index)
            elif to_second(row['测评时长']) < self.min_time:
                self.record.record[1].append(index)
                flag = True
                self.error_rows_record.add(index)

            # 筛选强制项不正确的
            for forced_i in self.forced_item:
                if row[df.columns[forced_i[0]]] != forced_i[1]:
                    self.record.record[2].append(index)
                    flag = True
                    self.error_rows_record.add(index)
                    # 只要有一个强制项不正确就可以结束判断了
                    break

            # 筛选重复项不一样的
            for repeat_i in self.repeat_item:
                if row[df.columns[repeat_i[0]]] != row[df.columns[repeat_i[1]]]:
                    self.record.record[3].append(index)
                    flag = True
                    self.error_rows_record.add(index)
                    # 只要有一对重复题不一致就可以结束判断了
                    break

            # 筛选重复率过高的
            choice_statistics = {}
            for i in range(1, self.question_count + 1):  # 先把每个问题选择的选项统计出来
                choice = int(row[df.columns[i]])
                if choice in choice_statistics:
                    choice_statistics[choice] = choice_statistics[choice] + 1
                else:
                    choice_statistics[choice] = 1

            choice_percentage = []
            for choice in choice_statistics:  # 然后要统计出每个选项选择的频率
                choice_percentage.append(choice_statistics[choice] / self.question_count)
            choice_percentage.sort()  # 排序选项出现频率
            if choice_percentage[-1] > self.same_percent:
                self.record.record[4].append(index)
                flag = True
                self.error_rows_record.add(index)

            if flag:
                df = df.drop(index)

        self.result_data = df
        self.result_rows = df.shape[0]

    def save_record(self):
        # error_description = {"原始数据行数": self.source_rows,
        #                      "有效数据行数": self.result_rows,
        #                      "无效数据行数": {str(len(self.error_rows_record)) + '行',
        #                                 ','.join(list(map(str, self.error_rows_record)))}
        #                      }
        error_description = [
            ["原始数据行数", str(self.source_rows)+'行'],
            ["有效数据行数", str(self.result_rows)+'行'],
            ["无效数据行数", str(len(self.error_rows_record)) + '行', ','.join(list(map(str, self.error_rows_record)))]

        ]
        df_1 = pd.DataFrame(data=error_description)
        error_type_statistics = []
        for i in range(len(self.record.error_type)):
            # error_type_statistics[0].append(str(self.record.error_type[i]) + '行数')
            # error_type_statistics[1].append([str(len(self.record.record[i])) + '行',
            #                                  ','.join(map(str, self.record.record[i]))])
            error_type_statistics.append([str(self.record.error_type[i]) + '行数', str(len(self.record.record[i])) + '行',
                                          ','.join(map(str, self.record.record[i]))])
        df_2 = pd.DataFrame(data=error_type_statistics)

        # 写统计数据文件
        with pd.ExcelWriter("Result/" + self.filename + " 数据筛选报告.xlsx") as writer:
            df_1.to_excel(writer, index=False, header=False)
            df_2.to_excel(writer, startrow=4, index=False, header=False)

        # 写原数据文件
        self.source_data.to_excel("Result/" + self.filename + " 原始数据.xlsx", index=False)
        # 写新数据文件
        self.result_data.to_excel("Result/" + self.filename + " 筛选数据.xlsx", index=False)


if __name__ == '__main__':
    filter = Filter(FileReader.read_source("Source/附件1(1).xlsx"), 23)
    print(filter.forced_item)
    print(filter.repeat_item)
    print(filter.source_rows)
