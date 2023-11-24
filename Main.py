import os

from util import FileReader
from processing.Filter import Filter
from GUI.build.build import welcome
from util.HighDPI import set_dpi_awareness
from util.FileReader import read_source


def start_processing():
    # path = "Source/"
    # files = os.listdir(path)
    # # 用了遍历的写法，事实上只能处理“一种格式”的问卷
    # for f in files:
    #     if '.xlsx' not in f:
    #         continue
    #     print(f)
    #     data = FileReader.read_source(path + f)
    #     filter = Filter(data, f[:-5], test=True)
    #     filter.get_questionnaire_info()
    #     filter.process()
    #     filter.save_record()
    set_dpi_awareness()
    welcome.start_window()


def test():
    filter = Filter(read_source(
        r"D:\WindStation\Documents\Pycharm\QuestionnaireFilter\Source\234274756_2_家庭教养方式测试（父母版）_245_245.xlsx"),
                    test=True)
    filter.build_basic_info()
    filter.build_condition()
    filter.get_questionnaire_info()
    filter.process()
    filter.save_record()


if __name__ == '__main__':
    start_processing()
