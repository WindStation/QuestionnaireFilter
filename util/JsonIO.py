import json


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        document = json.loads(f.read())

    return document


def write_json(path, document):
    """
    :param path: 从调用模块出发，到目标JSON文件的相对路径
    :param document: 要覆写的内容
    :return: None
    """
    with open(path, "w", encoding='utf-8') as f:
        f.write(json.dumps(document, ensure_ascii=False))


if __name__ == '__main__':
    dictionary = {"1": [1, 2, 3, 4, 5], "test": True}
    # write_json("../json/test.json", dictionary)

    document = read_json("../json/Condition.json")
    print(isinstance(document, dict))
    print(document)
