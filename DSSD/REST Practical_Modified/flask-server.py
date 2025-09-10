"""
REST API with Flask Framework
-----------------------------
This replaces http.server version.
Flask handles routing, JSON response, and headers automatically.
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory "database"
supermarket_items = [
{"id": 1, "name": "Milk (1L)", "category": "Dairy", "price": 2.50},
{"id": 2, "name": "Bread (White)", "category": "Bakery", "price": 1.75},
{"id": 3, "name": "Eggs (Dozen)", "category": "Dairy", "price": 4.00},
{"id": 4, "name": "Apples (1kg)", "category": "Produce", "price": 3.00},
{"id": 5, "name": "Chicken Breast (1kg)", "category": "Meat", "price": 8.00},
{"id": 6, "name": "Pasta (500g)", "category": "Pantry", "price": 1.20},
{"id": 7, "name": "Rice (1kg)", "category": "Pantry", "price": 2.00},
{"id": 8, "name": "Canned Tuna", "category": "Pantry", "price": 1.50},
{"id": 9, "name": "Orange Juice (1L)", "category": "Beverages", "price": 3.50},
{"id": 10, "name": "Coffee (250g)", "category": "Beverages", "price": 6.00},
{"id": 11, "name": "Cereal", "category": "Pantry", "price": 4.50},
{"id": 12, "name": "Yogurt", "category": "Dairy", "price": 1.00},
{"id": 13, "name": "Cheese (Cheddar, 250g)", "category": "Dairy", "price": 5.00},
{"id": 14, "name": "Bananas (1kg)", "category": "Produce", "price": 2.00},
{"id": 15, "name": "Ground Beef (1kg)", "category": "Meat", "price": 9.00},
{"id": 16, "name": "Tomato Sauce", "category": "Pantry", "price": 2.20},
{"id": 17, "name": "Olive Oil", "category": "Pantry", "price": 7.00},
{"id": 18, "name": "Soda (2L)", "category": "Beverages", "price": 2.75},
{"id": 19, "name": "Tea Bags (Box)", "category": "Beverages", "price": 4.00},
{"id": 20, "name": "Sugar (1kg)", "category": "Pantry", "price": 1.80},
{"id": 21, "name": "Salt", "category": "Pantry", "price": 1.00},
{"id": 22, "name": "Pepper", "category": "Pantry", "price": 1.50},
{"id": 23, "name": "Frozen Peas", "category": "Frozen", "price": 2.50},
{"id": 24, "name": "Ice Cream", "category": "Frozen", "price": 5.00},
{"id": 25, "name": "Butter", "category": "Dairy", "price": 3.20},
{"id": 26, "name": "Potatoes (1kg)", "category": "Produce", "price": 2.80},
{"id": 27, "name": "Carrots (1kg)", "category": "Produce", "price": 2.50},
{"id": 28, "name": "Onions (1kg)", "category": "Produce", "price": 2.20},
{"id": 29, "name": "Garlic", "category": "Produce", "price": 3.00},
{"id": 30, "name": "Lemons", "category": "Produce", "price": 4.00},
{"id": 31, "name": "Dish Soap", "category": "Household", "price": 3.50},
{"id": 32, "name": "Laundry Detergent", "category": "Household", "price": 8.00},
{"id": 33, "name": "Toilet Paper (6 Rolls)", "category": "Household", "price": 6.00},
{"id": 34, "name": "Shampoo", "category": "Personal Care", "price": 5.50},
{"id": 35, "name": "Conditioner", "category": "Personal Care", "price": 5.50},
{"id": 36, "name": "Toothpaste", "category": "Personal Care", "price": 3.00},
{"id": 37, "name": "Toothbrush", "category": "Personal Care", "price": 2.50},
{"id": 38, "name": "Paper Towels", "category": "Household", "price": 4.00},
{"id": 39, "name": "Trash Bags", "category": "Household", "price": 5.00},
{"id": 40, "name": "Hand Soap", "category": "Personal Care", "price": 2.00},
{"id": 41, "name": "Avocado", "category": "Produce", "price": 2.00},
{"id": 42, "name": "Bell Peppers", "category": "Produce", "price": 3.50},
{"id": 43, "name": "Cucumber", "category": "Produce", "price": 1.50},
{"id": 44, "name": "Broccoli", "category": "Produce", "price": 3.00},
{"id": 45, "name": "Spinach", "category": "Produce", "price": 2.50},
{"id": 46, "name": "Salmon (Fillet)", "category": "Seafood", "price": 12.00},
{"id": 47, "name": "Shrimp (1kg)", "category": "Seafood", "price": 15.00},
{"id": 48, "name": "Almonds (250g)", "category": "Snacks", "price": 6.00},
{"id": 49, "name": "Cashews (250g)", "category": "Snacks", "price": 7.00},
{"id": 50, "name": "Chips", "category": "Snacks", "price": 3.00},
{"id": 51, "name": "Chocolate Bar", "category": "Snacks", "price": 2.00},
{"id": 52, "name": "Crackers", "category": "Snacks", "price": 2.50},
{"id": 53, "name": "Peanut Butter", "category": "Pantry", "price": 4.00},
{"id": 54, "name": "Jelly", "category": "Pantry", "price": 3.50},
{"id": 55, "name": "Ketchup", "category": "Pantry", "price": 2.80},
{"id": 56, "name": "Mustard", "category": "Pantry", "price": 2.50},
{"id": 57, "name": "Mayonnaise", "category": "Pantry", "price": 3.00},
{"id": 58, "name": "Salad Dressing", "category": "Pantry", "price": 4.00},
{"id": 59, "name": "Pizza (Frozen)", "category": "Frozen", "price": 6.50},
{"id": 60, "name": "Waffles (Frozen)", "category": "Frozen", "price": 4.50}
]

# 1. GET all products
@app.route("/supermarket_items", methods=["GET"])
def get_supermarket_items():
    return jsonify(supermarket_items)   # Flask auto-converts Python list/dict to JSON

# 2. GET single product by ID
@app.route("/supermarket_items/<int:pid>", methods=["GET"])
def get_supermarket_item(pid):
    supermarket_item = next((p for p in supermarket_items if p["id"] == pid), None)
    if supermarket_item:
        return jsonify(supermarket_item)
    return jsonify({"error": "Product not found"}), 404

# 3. GET product by Category
@app.route("/supermarket_items/category/<category_name>", methods=["GET"])
def get_supermarket_items_by_category(category_name):
    items_in_category = [item for item in supermarket_items if item["category"].lower() == category_name.lower()] #Case-insensitive
 
    if items_in_category:
        return jsonify(items_in_category)
    return jsonify({"error": "No products found in this category"}), 404
 

# 4. POST - Add a new product
@app.route("/supermarket_items", methods=["POST"])
def add_supermarket_item():
    data = request.get_json()   # Flask automatically parses JSON body
    new_id = max([p["id"] for p in supermarket_items], default=0) + 1
    data["id"] = new_id
    supermarket_items.append(data)
    return jsonify(data), 201   # return created resource with status 201

# 5. PUT - Update a product
@app.route("/supermarket_items/<int:pid>", methods=["PUT"])
def update_supermarket_item(pid):
    supermarket_item = next((p for p in supermarket_items if p["id"] == pid), None)
    if not supermarket_item:
        return jsonify({"error": "supermarket_item not found"}), 404
    data = request.get_json()
    supermarket_item.update(data)
    return jsonify(supermarket_item)

# 6. DELETE - Remove a product
@app.route("/supermarket_items/<int:pid>", methods=["DELETE"])
def delete_supermarket_item(pid):
    global supermarket_items
    supermarket_items = [p for p in supermarket_items if p["id"] != pid]
    return jsonify({"message": "supermarket_item deleted"})

# Run server
if __name__ == "__main__":
    app.run(debug=True, port=5000)