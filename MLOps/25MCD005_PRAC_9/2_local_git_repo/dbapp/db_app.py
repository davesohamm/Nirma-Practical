from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://mongodb:27017/")
db = client["iris_db"]
collection = db["predictions"]

@app.route("/store", methods=["POST"])
def store():
    data = request.json
    collection.insert_one(data)
    return jsonify({"message": "Stored successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)