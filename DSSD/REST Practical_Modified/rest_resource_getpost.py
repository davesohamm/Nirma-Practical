'''
Demonstration: Resource-Based REST API
'''

from flask import Flask, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# -----------------------------------
# In-Memory "Database" (for demo only)
# -----------------------------------
users_db = [
    {"name": "Soham", "age": 21, "occupation": "Software Developer"},
    {"name": "Ishaan", "age": 25, "occupation": "Data Scientist"},
    {"name": "Riya", "age": 28, "occupation": "UI/UX Designer"}
]

todos = {}  # simple dictionary to store todo tasks


# -------------------------------
# Simple Example Resource
# -------------------------------
class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello, API world!"}, 200


# -------------------------------
# User Resource (CRUD Operations)
# -------------------------------
class User(Resource):

    # Read data (single user or full list)
    def get(self, name=None):
        if name:
            for user in users_db:
                if user["name"].lower() == name.lower():
                    return {"user": user}, 200
            return {"error": f"User '{name}' not found."}, 404
        return {"users": users_db}, 200


    # Create a new user
    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age", required=True, help="Age field is required.")
        parser.add_argument("occupation", required=True, help="Occupation field is required.")
        args = parser.parse_args()

        for user in users_db:
            if user["name"].lower() == name.lower():
                return {"error": f"User '{name}' already exists."}, 400

        new_user = {"name": name, "age": args["age"], "occupation": args["occupation"]}
        users_db.append(new_user)
        return {"message": f"User '{name}' added successfully.", "user": new_user}, 201


    # Update or replace user data
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users_db:
            if user["name"].lower() == name.lower():
                user["age"] = args["age"] or user["age"]
                user["occupation"] = args["occupation"] or user["occupation"]
                return {"message": f"User '{name}' updated successfully.", "user": user}, 200

        # If user doesn't exist, create new entry
        new_user = {"name": name, "age": args["age"], "occupation": args["occupation"]}
        users_db.append(new_user)
        return {"message": f"User '{name}' created (was not found earlier).", "user": new_user}, 201


    # Delete a user
    def delete(self, name):
        global users_db
        filtered_users = [u for u in users_db if u["name"].lower() != name.lower()]

        if len(filtered_users) == len(users_db):
            return {"error": f"User '{name}' not found."}, 404

        users_db = filtered_users
        return {"message": f"User '{name}' deleted successfully."}, 200


# -------------------------------
# Todo Resource (Single + List)
# -------------------------------
class TodoItem(Resource):
    def get(self, todo_id):
        if todo_id not in todos:
            return {"error": f"Todo with ID '{todo_id}' not found."}, 404
        return {"todo_id": todo_id, "task": todos[todo_id]}, 200

    def post(self, todo_id):
        if 'task' not in request.form:
            return {"error": "Missing 'task' parameter in request."}, 400

        todos[todo_id] = request.form['task']
        return {"message": f"Task '{todo_id}' added.", "task": todos[todo_id]}, 201


class TodoList(Resource):
    def get(self):
        return {"todos": todos}, 200


# -------------------------------
# Additional Routes
# -------------------------------
@app.route('/')
def home():
    return (
        "Welcome to Soham's REST API Demo!<br>"
        "Available endpoints:<br>"
        "- /user or /user/<name><br>"
        "- /todos or /todos/<id><br>"
        "- /hello or /greet<br>"
    )


@app.route('/hi')
def greet():
    return "Hey there! The API is live and working perfectly."


# -------------------------------
# Resource Mappings
# -------------------------------
api.add_resource(HelloWorld, '/hello', '/greet')
api.add_resource(User, '/user', '/user/<string:name>')
api.add_resource(TodoList, '/todos')
api.add_resource(TodoItem, '/todos/<string:todo_id>', '/<string:todo_id>')


# -------------------------------
# Run the App
# -------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
