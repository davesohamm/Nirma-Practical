from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# In-memory database (list of dicts)
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

# Utility: find product by id
def find_item(pid):
    return next((item for item in supermarket_items if item["id"] == pid), None)

class MyHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # Handle GET
    def do_GET(self):
        if self.path == "/supermarket_items":
            self.send_json(supermarket_items)

        elif self.path.startswith("/supermarket_items/category/"):
            category = self.path.split("/")[-1]
            items = [item for item in supermarket_items if item["category"].lower() == category.lower()]
            if items:
                self.send_json(items)
            else:
                self.send_json({"error": f"No items found in category '{category}'"}, 404)

        elif self.path.startswith("/supermarket_items/"):
            try:
                pid = int(self.path.split("/")[-1])
                item = find_item(pid)
                if item:
                    self.send_json(item)
                else:
                    self.send_json({"error": "Item not found"}, 404)
            except:
                self.send_json({"error": "Invalid ID"}, 400)

        else:
            self.send_json({"error": "Not found"}, 404)

    # Handle POST (add new product)
    def do_POST(self):
        if self.path == "/supermarket_items":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                new_id = max([item["id"] for item in supermarket_items], default=0) + 1
                data["id"] = new_id
                supermarket_items.append(data)
                self.send_json(data, 201)
            except:
                self.send_json({"error": "Invalid JSON"}, 400)
        else:
            self.send_json({"error": "Not found"}, 404)

    # Handle PUT (update product)
    def do_PUT(self):
        if self.path.startswith("/supermarket_items/"):
            try:
                pid = int(self.path.split("/")[-1])
                item = find_item(pid)
                if not item:
                    self.send_json({"error": "Item not found"}, 404)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                put_data = self.rfile.read(content_length)
                data = json.loads(put_data)
                item.update(data)
                self.send_json(item)
            except:
                self.send_json({"error": "Invalid request"}, 400)
        else:
            self.send_json({"error": "Not found"}, 404)

    # Handle DELETE
    def do_DELETE(self):
        if self.path.startswith("/supermarket_items/"):
            try:
                pid = int(self.path.split("/")[-1])
                item = find_item(pid)
                if item:
                    supermarket_items.remove(item)
                    self.send_json({"message": "Item deleted"})
                else:
                    self.send_json({"error": "Item not found"}, 404)
            except:
                self.send_json({"error": "Invalid ID"}, 400)
        else:
            self.send_json({"error": "Not found"}, 404)


if __name__ == "__main__":
    server = HTTPServer(("localhost", 5000), MyHandler)
    print("Server running at http://localhost:5000")
    server.serve_forever()
