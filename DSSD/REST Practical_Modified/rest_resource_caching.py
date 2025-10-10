'''
Author: Soham Dave
Demonstration of Resource-Based REST API with Caching
----------------------------------------------------
Concepts Shown:
  1. Client-side caching (HTTP headers like Cache-Control)
  2. Server-side caching using Flask-Caching (in-memory demo)
  
Note:
  - This example uses simple in-memory storage (no database).
  - Demonstrates how caching improves API response speed.
'''

from flask import Flask, make_response, request
from flask_restful import Api, Resource, reqparse
from flask_caching import Cache
import time

# -----------------------
# App and Cache Setup
# -----------------------
app = Flask(__name__)
api = Api(app)

app.config["CACHE_TYPE"] = "SimpleCache"       # in-memory caching
app.config["CACHE_DEFAULT_TIMEOUT"] = 60       # default 1-minute cache
cache = Cache(app)

# -----------------------
# In-Memory Data (Custom)
# -----------------------
users_db = [
    {"username": "Soham", "age": 21, "role": "Developer"},
    {"username": "Priya", "age": 28, "role": "Designer"},
    {"username": "Rahul", "age": 26, "role": "Tester"}
]

todo_tasks = {}  # stores tasks by ID


# -----------------------
# Utility print
# -----------------------
def log_action(action, data=""):
    print(f"[Server Log] {action} --> {data}")


# -----------------------
# Resource Classes
# -----------------------
class Home(Resource):
    def get(self):
        return {
            "message": "Welcome to Soham's REST API Demo! Use /users or /todos endpoints."
        }


class HelloWorld(Resource):
    def get(self):
        log_action("GET /hello", "Hello endpoint triggered")
        return {"greeting": "Hello from Soham's API!"}, 200


class User(Resource):
    def get(self, username=None):
        """
        GET /users        → returns all users (cached for 60 sec)
        GET /users/<name> → returns details for one user
        """
        if username:
            for user in users_db:
                if user["username"].lower() == username.lower():
                    log_action("Fetched user", username)
                    return user, 200
            log_action("User not found", username)
            return {"error": f"User '{username}' not found"}, 404

        # If no username, return all users with Cache-Control header
        response = make_response(users_db, 200)
        response.headers["Cache-Control"] = "public, max-age=60"
        log_action("Returned full user list (cached 60s)")
        return response

    def post(self, username):
        """
        POST /users/<name> - Adds a new user
        Data: {"age": <int>, "role": <str>}
        """
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("role")
        args = parser.parse_args()

        for user in users_db:
            if user["username"].lower() == username.lower():
                log_action("Duplicate user attempt", username)
                return {"error": f"User '{username}' already exists"}, 400

        new_user = {"username": username, "age": args["age"], "role": args["role"]}
        users_db.append(new_user)
        log_action("Added new user", new_user)
        return new_user, 201

    def put(self, username):
        """
        PUT /users/<name> - Updates or creates user
        """
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("role")
        args = parser.parse_args()

        for user in users_db:
            if user["username"].lower() == username.lower():
                user["age"] = args["age"]
                user["role"] = args["role"]
                log_action("Updated user", username)
                return user, 200

        new_user = {"username": username, "age": args["age"], "role": args["role"]}
        users_db.append(new_user)
        log_action("Created user (via PUT)", new_user)
        return new_user, 201

    def delete(self, username):
        """
        DELETE /users/<name> - Removes user
        """
        global users_db
        users_db = [u for u in users_db if u["username"].lower() != username.lower()]
        log_action("Deleted user", username)
        return {"message": f"User '{username}' removed successfully"}, 200


class TodoTask(Resource):
    @cache.cached(timeout=60, query_string=True)
    def get(self, task_id):
        """
        GET /todos/<id> - Returns task info (cached for 60s)
        """
        if task_id not in todo_tasks:
            log_action("Task not found", task_id)
            return {"error": "Task not found"}, 404
        log_action("Fetched todo task (cached)", task_id)
        return {"cached_at": time.time(), task_id: todo_tasks[task_id]}, 200

    def post(self, task_id):
        """
        POST /todos/<id> - Adds a new task
        """
        todo_tasks[task_id] = request.form["task"]
        log_action("Added new task", {task_id: todo_tasks[task_id]})
        return {task_id: todo_tasks[task_id]}, 201


class TodoList(Resource):
    def get(self):
        log_action("Fetched all todos", todo_tasks)
        return todo_tasks, 200


# -----------------------
# Routes and Endpoints
# -----------------------
api.add_resource(Home, "/")
api.add_resource(HelloWorld, "/hello")
api.add_resource(User, "/users", "/users/<string:username>")
api.add_resource(TodoList, "/todos")
api.add_resource(TodoTask, "/todos/<string:task_id>")

# -----------------------
# Run App
# -----------------------
if __name__ == "__main__":
    log_action("Starting Flask REST API", "Running on port 5001")
    app.run(host="0.0.0.0", port=5001, debug=True)
