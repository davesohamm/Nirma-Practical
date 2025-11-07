from pymongo import MongoClient
from pymongo.read_concern import ReadConcern

client = MongoClient("mongodb://localhost:27010")  # or connect directly to mongod secondary host
db_majority = client.get_database("testdb", read_concern=ReadConcern("majority"))
coll = db_majority.rc_test

# Read with majority read concern
for doc in coll.find():
    print("majority-read:", doc)

# Read with default (local) read concern using a normal DB handle
db_local = client["testdb"]
for doc in db_local.rc_test.find():
    print("local-read:", doc)
