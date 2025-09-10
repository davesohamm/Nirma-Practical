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
    print("\n==== supermarket_item MANAGEMENT MENU ====")
    print("1. Show all supermarket_items")
    print("2. Get supermarket_item by ID")
    print("3. Get supermarket_items by Category")
    print("4. Add new supermarket_item")
    print("5. Update supermarket_item")
    print("6. Delete supermarket_item")
    print("7. Exit")

def get_all_supermarket_items():
    res = requests.get(f"{BASE_URL}/supermarket_items")
    print("supermarket_items:", res.json())

def get_supermarket_item():
    pid = input("Enter supermarket_item ID: ")
    res = requests.get(f"{BASE_URL}/supermarket_items/{pid}")
    print("Response:", res.json())

def get_supermarket_items_by_category():
    category = input("Enter the category you want to search for (Dairy, Bakery, Produce, Meat, Pantry, Beverages, Frozen, Household, Personal Care, Seafood, Snacks): ")
    res = requests.get(f"{BASE_URL}/supermarket_items/category/{category}")
    if res.status_code == 200:
        print(f"Items in the '{category}' category:", res.json())
    elif res.status_code == 404:
        print(f"No products found in the '{category}' category.")
    else:
        print(f"Error: {res.status_code} - {res.json()}")

def add_supermarket_item():
    name = input("Enter supermarket_item name: ")
    price = float(input("Enter supermarket_item price: "))
    category = str(input("Which Category? (Dairy, Bakery, Produce, Meat, Pantry, Beverages, Frozen, Household, Personal Care, Seafood, Snacks) :"))
    supermarket_item = {"name": name, "category": category, "price": price}
    res = requests.post(f"{BASE_URL}/supermarket_items", json=supermarket_item)
    print("Response:", res.json())

def update_supermarket_item():
    pid = input("Enter supermarket_item ID to update: ")
    field = input("Enter field to update (name/price/category): ")
    value = input("Enter new value: ")
    
    # Convert price to number if field is price
    data = {field: float(value) if field == "price" else value}
    res = requests.put(f"{BASE_URL}/supermarket_items/{pid}", json=data)
    print("Response:", res.json())

def delete_supermarket_item():
    pid = input("Enter supermarket_item ID to delete: ")
    res = requests.delete(f"{BASE_URL}/supermarket_items/{pid}")
    print("Response:", res.json())

# Main loop
if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            get_all_supermarket_items()
        elif choice == "2":
            get_supermarket_item()
        elif choice == "3":
            get_supermarket_items_by_category()
        elif choice == "4":
            add_supermarket_item()
        elif choice == "5":
            update_supermarket_item()
        elif choice == "6":
            delete_supermarket_item()
        elif choice == "7":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")