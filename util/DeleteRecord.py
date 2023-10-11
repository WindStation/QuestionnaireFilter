import json


class DeleteRecord:
    def __init__(self):
        self.error_type = json.loads(open("../json/ErrorType.json", 'r', encoding='utf-8').read())
        self.record = {
            0: list(),
            1: list(),
            2: list(),
            3: list(),
            4: list(),
        }
