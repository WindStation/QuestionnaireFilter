from datetime import datetime


class FilterRec:
    def __init__(self, prev_cnt, invalid_cnt):
        self.gmt_created = datetime.now()
        self.prev_cnt = prev_cnt
        self.invalid_cnt = invalid_cnt
