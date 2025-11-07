from pymongo import MongoClient, WriteConcern
from pymongo.errors import PyMongoError

client = MongoClient("mongodb://localhost:27011", serverSelectionTimeoutMS=5000)
db = client["testdb"]
coll = db.get_collection("tconf_comb", write_concern=WriteConcern(w=3, wtimeout=5000))

try:
    coll.insert_one({"test":"combined_failover", "ts":__import__('datetime').datetime.utcnow()})
    print("Write succeeded")
except PyMongoError as e:
    print("Write failed or timed out:", type(e).__name__, str(e))
