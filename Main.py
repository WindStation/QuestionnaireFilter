import os

import FileReader
from Filter import Filter

if __name__ == '__main__':
    data = FileReader.read_source("Source/附件1(1).xlsx")
    filter = Filter(data, 23)
    filter.process()
    filter.save_record()
