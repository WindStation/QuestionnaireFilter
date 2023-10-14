from datetime import datetime


class FilterRec:
    def __init__(self, prev_cnt, invalid_cnt, error_rec):
        self.gmt_created = str(datetime.now())
        self.prev_cnt = prev_cnt
        self.invalid_cnt = invalid_cnt
        # error_rec这个与DeleteRecord里的record有点功能重复，都是用dict来记录每种不符合规则的序号
        # 这里是{规则名: [序号]}的格式，而record是{index(0~len): [序号]}的格式
        self.error_rec = error_rec
