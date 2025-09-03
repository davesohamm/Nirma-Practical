from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# In-memory "database" as a dictionary
# Key = product ID, Value = dict with product details
products = {
    1: {"id": 1, "name": "Laptop", "price": 1000},
    2: {"id": 2, "name": "Phone", "price": 500}
}

class MyHandler(BaseHTTPRequestHandler):

    # Utility: Send JSON response
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # Handle GET
    def do_GET(self):
        if self.path == "/products":
            # Return all products
            self.send_json(list(products.values()))   # dict → list of values
        elif self.path.startswith("/products/"):
            try:
                pid = int(self.path.split("/")[-1])
                if pid in products:
                    self.send_json(products[pid])
                else:
                    self.send_json({"error": "Product not found"}, 404)
            except:
                self.send_json({"error": "Invalid ID"}, 400)
        else:
            self.send_json({"error": "Not found"}, 404)

    # Handle POST (add new product)
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data)
            new_id = max(products.keys(), default=0) + 1
            data["id"] = new_id
            products[new_id] = data
            self.send_json(data, 201)
        except:
            self.send_json({"error": "Invalid JSON"}, 400)

    # Handle PUT (update product)
    def do_PUT(self):
        if self.path.startswith("/products/"):
            try:
                pid = int(self.path.split("/")[-1])
                if pid not in products:
                    self.send_json({"error": "Product not found"}, 404)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                put_data = self.rfile.read(content_length)
                data = json.loads(put_data)
                products[pid].update(data)
                self.send_json(products[pid])
            except:
                self.send_json({"error": "Invalid request"}, 400)
        else:
            self.send_json({"error": "Not found"}, 404)

    # Handle DELETE
    def do_DELETE(self):
        if self.path.startswith("/products/"):
            try:
                pid = int(self.path.split("/")[-1])
                if pid in products:
                    del products[pid]
                    self.send_json({"message": "Product deleted"})
                else:
                    self.send_json({"error": "Product not found"}, 404)
            except:
                self.send_json({"error": "Invalid ID"}, 400)
        else:
            self.send_json({"error": "Not found"}, 404)


# Run the server
if __name__ == "__main__":
    server = HTTPServer(("localhost", 5000), MyHandler)
    print("Server running at http://localhost:5000")
    server.serve_forever()
