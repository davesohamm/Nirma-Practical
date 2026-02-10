# server1.py / server2.py / server3.py
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load data from a JSON file (create accounts.json if not available)
with open("accounts.json", "r") as f:
    raw_data = json.load(f)

accounts = {acc["account_id"]: acc for acc in raw_data}


@app.route("/accounts", methods=["GET"])
def get_accounts():
    return jsonify(list(accounts.values()))


@app.route("/accounts/<int:aid>", methods=["GET"])
def get_account(aid):
    account = accounts.get(aid)
    if account:
        return jsonify(account)
    return jsonify({"error": "Account not found"}), 404


@app.route("/accounts", methods=["POST"])
def add_account():
    try:
        data = request.get_json()
        new_id = max(accounts.keys(), default=0) + 1
        data["account_id"] = new_id
        accounts[new_id] = data
        return jsonify(accounts[new_id]), 201
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400


@app.route("/accounts/<int:aid>", methods=["PUT"])
def update_account(aid):
    account = accounts.get(aid)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    try:
        data = request.get_json()
        account.update(data)
        return jsonify(account)
    except Exception:
        return jsonify({"error": "Invalid request"}), 400


@app.route("/accounts/<int:aid>", methods=["DELETE"])
def delete_account(aid):
    if aid in accounts:
        del accounts[aid]
        return jsonify({"message": "Account deleted"})
    return jsonify({"error": "Account not found"}), 404


if __name__ == "__main__":
    # Run each server on different ports
    app.run(debug=True, port=5001)  # Change to 5002 or 5003 for other servers
