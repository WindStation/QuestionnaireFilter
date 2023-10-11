import pandas as pd
from pandas import DataFrame


def read_source(filename):
    # filename = "Source/测试问卷1.xlsx"
    data = pd.read_excel(filename)
    print(data)
    print(data.describe())
    return data


# Deprecated
def write_source(filename, data):
    filepath = "../Result/"
    data.to_excel(filepath + filename, index=False)


if __name__ == '__main__':
    data = read_source("Source/测试问卷1.xlsx")
    write_source("结果.xlsx", data)
