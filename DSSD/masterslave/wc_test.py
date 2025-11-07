from pymongo import MongoClient, WriteConcern
from pymongo.errors import WriteConcernError, ServerSelectionTimeoutError

client = MongoClient("mongodb://localhost:27020")  # connect to mongos or primary mongod
db = client["testdb"]

# Collection with explicit write concern w=3 (requires acknowledgement from 3 members)
coll_wc = db.get_collection("tconf_wc_py").with_options(write_concern=WriteConcern(w=3, wtimeout=5000))

try:
    result = coll_wc.insert_one({"name":"wc_test_py", "ts":__import__('datetime').datetime.utcnow()})
    print("Insert acknowledged, _id:", result.inserted_id)
except WriteConcernError as e:
    print("WriteConcernError:", e)
except Exception as e:
    print("Other error:", type(e).__name__, e)
