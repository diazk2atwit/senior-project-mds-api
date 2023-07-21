import json
from pprint import pprint
from decouple import config
from pymongo import MongoClient

#############
#   Keys    #
#############
DB_KEY = config('MONGODB_PWD')


#############################
# MongoDB Client Connection #
#############################
connection_string = f"mongodb+srv://diazk2:{DB_KEY}@cluster0.qmguqff.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)


###########################
# Database and Collection #
###########################
production_db = client["production"]  # Production Database

file_collection = production_db["file_collection"]  # File Collection
url_collection = production_db["url_collection"]  # URL Collection


#############
# Functions #
#############
# def create_documents():
#     first_names = ["Kevin", "Alex", "Rick", "Ross", "Boss"]
#     last_names = ["Diaz", "Polly", "Klockstar", "Moss", "Juice"]
#     ages = [22, 23, 24, 25, 26]
#
#     docs = []
#
#     for first_name, last_name, age in zip(first_names, last_names, ages):
#         doc = {"first_name": first_name, "last_name": last_name, "age": age}
#         docs.append(doc)
#     print(docs)
#     person_collection.insert_many(docs)


# def insert_test_doc():
#     collection = test_db["test"]
#     test_document = {
#         "name": "Kevin",
#         "type": "Test"
#     }
#     inserted_id = collection.insert_one(test_document).inserted_id
#     print(inserted_id)


def insert_url_doc(web_url, result):
    temp = {"web_url": web_url}
    document = dict(result)
    document.update(temp)

    url_collection.insert_one(document)


def insert_file_doc(hash_file, result):
    temp = {"hash_file": hash_file}
    document = dict(result)
    document.update(temp)

    file_collection.insert_one(document)


def get_url_doc(url):
    document = url_collection.find_one({"web_url": url}, {"_id": 0})
    return document
    # pprint(document)


def get_file_doc(hash_file):
    document = file_collection.find_one({"hash_file": hash_file}, {"_id": 0})
    return document
    # pprint(document)


# def find_all_people():
#     people = person_collection.find()
#
#     for person in people:
#         pprint(person)


# def find_kevin():
#     kevin = person_collection.find_one({"first_name": "Kevin"})
#     pprint(kevin)


# def count_all_people():
#     count = person_collection.count_documents(filter={})
#     print(f"Number of people: {count}")


# def get_person_by_id(person_id):
#     from bson.objectid import ObjectId
#     _id = ObjectId(person_id)
#
#     person = person_collection.find_one({"_id": _id})
#     pprint(person)


# def get_age_range(min_age, max_age):
#     query = {"$and": [
#                 {"age": {"$gte": min_age}},
#                 {"age": {"$lte": max_age}}
#             ]}
#
#     people = person_collection.find(query).sort("age")
#     for person in people:
#         pprint(person)


# def project_columns():
#     columns = {"_id": 0, "first_name": 1, "last_name": 1}
#     people = person_collection.find({}, columns)
#     for person in people:
#         pprint(person)


#############
# Debugging #
#############
if __name__ == "__main__":
    print("Debugging:")
