import os

import FileReader
from Filter import Filter

if __name__ == '__main__':
    path = "Source/"
    files = os.listdir(path)
    # 用了遍历的写法，事实上只能处理“一种格式”的问卷
    for f in files:
        if '.xlsx' not in f:
            continue
        print(f)
        data = FileReader.read_source(path + f)
        filter = Filter(data, f[:-5])
        filter.process()
        filter.save_record()
