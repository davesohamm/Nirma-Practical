'''
Demonstration: Resource-Based REST API
Feature Shown: API Versioning (v1 and v2)
'''

from flask import Flask, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# ---------------------------
# Simulated In-Memory Database
# ---------------------------
users_data = [
    {"name": "Soham", "age": 21, "occupation": "Developer"},
    {"name": "Ishaan", "age": 25, "occupation": "Data Analyst"},
    {"name": "Riya", "age": 28, "occupation": "UI Designer"}
]

tasks = {}   # Task dictionary for demo


# ---------------------------
# Example Resource: HelloWorld
# ---------------------------
class HelloWorld(Resource):
    def get(self):
        return {"message": "Hey there, world!"}, 200


# ---------------------------
# User Resource (CRUD + Versioning)
# ---------------------------
class User(Resource):

    def get(self, name=None):
        # Check API version from URL
        api_version = "v1" if "/v1/" in request.path else "v2"

        if name:
            for user in users_data:
                if user["name"].lower() == name.lower():
                    # v1 returns age, v2 returns occupation
                    if api_version == "v1":
                        return {"name": user["name"], "age": user["age"]}, 200
                    else:
                        return {"name": user["name"], "occupation": user["occupation"]}, 200
            return {"error": f"User '{name}' not found."}, 404

        return {"users": users_data}, 200


    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age", required=True, help="Age field is required.")
        parser.add_argument("occupation", required=True, help="Occupation field is required.")
        args = parser.parse_args()

        for user in users_data:
            if user["name"].lower() == name.lower():
                return {"error": f"User '{name}' already exists."}, 400

        new_user = {"name": name, "age": args["age"], "occupation": args["occupation"]}
        users_data.append(new_user)
        return {"message": f"User '{name}' added successfully!", "user": new_user}, 201


    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users_data:
            if user["name"].lower() == name.lower():
                user["age"] = args["age"] or user["age"]
                user["occupation"] = args["occupation"] or user["occupation"]
                return {"message": f"User '{name}' updated successfully!", "user": user}, 200

        new_user = {"name": name, "age": args["age"], "occupation": args["occupation"]}
        users_data.append(new_user)
        return {"message": f"User '{name}' created (not found earlier).", "user": new_user}, 201


    def delete(self, name):
        global users_data
        updated_list = [u for u in users_data if u["name"].lower() != name.lower()]

        if len(updated_list) == len(users_data):
            return {"error": f"User '{name}' not found for deletion."}, 404

        users_data = updated_list
        return {"message": f"User '{name}' deleted successfully."}, 200


# ---------------------------
# Todo Resources
# ---------------------------
class TodoItem(Resource):
    def get(self, task_id):
        if task_id not in tasks:
            return {"error": f"No task found with ID {task_id}."}, 404
        return {"task_id": task_id, "task": tasks[task_id]}, 200

    def post(self, task_id):
        if 'task' not in request.form:
            return {"error": "Missing 'task' parameter in request."}, 400

        tasks[task_id] = request.form['task']
        return {"message": f"Task '{task_id}' added.", "task": tasks[task_id]}, 201


class TodoList(Resource):
    def get(self):
        return {"tasks": tasks}, 200


# ---------------------------
# Additional Routes
# ---------------------------
@app.route('/')
def home():
    return (
        "Welcome to the User & Todo REST API Demo!<br>"
        "Try endpoints like:<br>"
        "- /v1/user/Soham (get age)<br>"
        "- /v2/user/Soham (get occupation)<br>"
        "- /todos or /todos/<id>"
    )


# ---------------------------
# Endpoint Mapping
# ---------------------------
api.add_resource(HelloWorld, '/hello', '/greet')
api.add_resource(User, "/user", "/v1/user/<string:name>", "/v2/user/<string:name>")
api.add_resource(TodoList, '/todos')
api.add_resource(TodoItem, '/todos/<string:task_id>', '/<string:task_id>')

# Run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
