"""
Menu-driven client to interact with REST API server
-----------------------------------------------------
- Connects to http://127.0.0.1:5000
- Supports CRUD operations on products
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def show_menu():
    print("\n==== PRODUCT MANAGEMENT MENU ====")
    print("1. Show all products")
    print("2. Get product by ID")
    print("3. Add new product")
    print("4. Update product")
    print("5. Delete product")
    print("6. Exit")

def get_all_products():
    res = requests.get(f"{BASE_URL}/products")
    print("Products:", res.json())

def get_product():
    pid = input("Enter Product ID: ")
    res = requests.get(f"{BASE_URL}/products/{pid}")
    print("Response:", res.json())

def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    product = {"name": name, "price": price}
    res = requests.post(f"{BASE_URL}/products", json=product)
    print("Response:", res.json())

def update_product():
    pid = input("Enter Product ID to update: ")
    field = input("Enter field to update (name/price): ")
    value = input("Enter new value: ")
    
    # Convert price to number if field is price
    data = {field: float(value) if field == "price" else value}
    res = requests.put(f"{BASE_URL}/products/{pid}", json=data)
    print("Response:", res.json())

def delete_product():
    pid = input("Enter Product ID to delete: ")
    res = requests.delete(f"{BASE_URL}/products/{pid}")
    print("Response:", res.json())

# Main loop
if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            get_all_products()
        elif choice == "2":
            get_product()
        elif choice == "3":
            add_product()
        elif choice == "4":
            update_product()
        elif choice == "5":
            delete_product()
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")