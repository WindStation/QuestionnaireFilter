import pymongo
from bson import ObjectId
from pymongo import MongoClient
from model import Questionnaire, AnswerRec, FilterRec


def get_connection():
    client = MongoClient('localhost', 27017,
                         maxPoolSize=10)
    print("已建立连接")
    return client


def get_collection(client: MongoClient, collection_name):
    db = client.get_database('questionnaire')
    collection = db.get_collection(collection_name)
    return collection


def insert(document):
    db = get_connection()
    collection = get_collection(db, 'questionnaire')
    result = collection.insert_one(document)

    db.close()
    return result


def default(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError("Object of type {} is not JSON serializable".format(type(obj)))


if __name__ == '__main__':
    collection = get_collection(get_connection(), 'questionnaire')
    ansrecs = [AnswerRec.AnswerRec(1, ["3", "2", "1"]).__dict__, AnswerRec.AnswerRec(2, ["3", "1", "2"]).__dict__,
               AnswerRec.AnswerRec(3, ["4", "6", "2"]).__dict__]
    filters = FilterRec.FilterRec(4, 1, {
        "规则1": [],
        "规则2": [1]
    })
    ques = Questionnaire.Questionnaire(["问题1", "问题2", "问题3"], ansrecs, filters.__dict__)
    print(ques.__dict__)

    collection.insert_one(ques.__dict__)
    for item in collection.find():
        print(item)
