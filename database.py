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


def get_file_doc(hash_file):
    document = file_collection.find_one({"hash_file": hash_file}, {"_id": 0})
    return document


#############
# Debugging #
#############
if __name__ == "__main__":
    print("Debugging:")
