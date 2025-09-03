"""
REST API with Flask Framework
-----------------------------
This replaces http.server version.
Flask handles routing, JSON response, and headers automatically.
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory "database"
products = [
    {"id": 1, "name": "Laptop", "price": 1000},
    {"id": 2, "name": "Phone", "price": 500}
]

# 1. GET all products
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)   # Flask auto-converts Python list/dict to JSON

# 2. GET single product by ID
@app.route("/products/<int:pid>", methods=["GET"])
def get_product(pid):
    product = next((p for p in products if p["id"] == pid), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

# 3. POST - Add a new product
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()   # Flask automatically parses JSON body
    new_id = max([p["id"] for p in products], default=0) + 1
    data["id"] = new_id
    products.append(data)
    return jsonify(data), 201   # return created resource with status 201

# 4. PUT - Update a product
@app.route("/products/<int:pid>", methods=["PUT"])
def update_product(pid):
    product = next((p for p in products if p["id"] == pid), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    data = request.get_json()
    product.update(data)
    return jsonify(product)

# 5. DELETE - Remove a product
@app.route("/products/<int:pid>", methods=["DELETE"])
def delete_product(pid):
    global products
    products = [p for p in products if p["id"] != pid]
    return jsonify({"message": "Product deleted"})

# Run server
if __name__ == "__main__":
    app.run(debug=True, port=5000)