from pymongo import MongoClient
from datetime import datetime, timedelta
import re

def connect_to_mongodb():
    # Connect to local MongoDB (default host and port)
    return MongoClient("mongodb://localhost:27017/")

def connect_to_maindb():
    return MongoClient("mongodb://admin:q8vm5dz-h29piX%3FMo%26%3ClO4e0zn@mongodb4:27017,arbiter:27017/zeno_db?authSource=admin&replicaSet=rs1")

def insert_document(db, collection, document):
    inserted_id = collection.insert_one(document).inserted_id
    print(f"Inserted document ID: {inserted_id}")
    return

def check_if_document_exist(db, collection, document):
    item = collection.find_one(document)
    if item:
        return 1
    else:
        return 0

def clean_url(url):
    url = re.sub('https', 'http', url)
    url = re.sub('//www.', '//', url)
    url = url.rstrip('/')
    return url

def format_date(datestr):

    now = datetime.now()
    datestr_split = datestr.split(' ')

    if datestr_split[1]=='day' or datestr_split[1]=='days':
        _date = now - timedelta(days=int(datestr_split[0]))
    elif datestr_split[1]=='hour' or datestr_split[1]=='hours':
        _date = now - timedelta(hours=int(datestr_split[0]))
    elif datestr_split[1]=='minute' or datestr_split[1]=='minutes':
        _date = now - timedelta(minutes=int(datestr_split[0]))
    elif datestr_split[1]=='second' or datestr_split[1]=='seconds':
        _date = now - timedelta(seconds=int(datestr_split[0]))
    else:
        pass   

    return _date.date()

def get_url_response(page, url):
    return page.goto(url, wait_until="domcontentloaded", timeout=60000)




# # Choose (or create) a database
# db = client["mydatabase"]

# # Choose (or create) a collection (like a SQL table)
# collection = db["customers"]

# # Insert a document
# doc = {"name": "Jonathan", "address": "Philippines"}
# inserted_id = collection.insert_one(doc).inserted_id
# print(f"Inserted document ID: {inserted_id}")

# # Find a document
# result = collection.find_one({"name": "Jonathan"})
# print(result)
