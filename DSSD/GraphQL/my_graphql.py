from flask import Flask, request, jsonify
import graphene

# -------------------------------
# In-memory "database" (dictionary)
# -------------------------------
products_db = {
    1: {"id": 1, "name": "Coffee Maker", "price": 80},
    2: {"id": 2, "name": "Toaster", "price": 45},
    3: {"id": 3, "name": "Blender", "price": 65},
    4: {"id": 4, "name": "Air Fryer", "price": 120},
    5: {"id": 5, "name": "Vacuum Cleaner", "price": 150},
    6: {"id": 6, "name": "Desk Lamp", "price": 35},
    7: {"id": 7, "name": "Desk Chair", "price": 200},
    8: {"id": 8, "name": "Dining Table", "price": 350},
    9: {"id": 9, "name": "Area Rug", "price": 100},
    10: {"id": 10, "name": "Microwave Oven", "price": 180},
    11: {"id": 11, "name": "Electric Kettle", "price": 30},
    12: {"id": 12, "name": "Slow Cooker", "price": 60},
    13: {"id": 13, "name": "Food Processor", "price": 110},
    14: {"id": 14, "name": "Espresso Machine", "price": 250},
    15: {"id": 15, "name": "Juicer", "price": 85},
    16: {"id": 16, "name": "Stand Mixer", "price": 220},
    17: {"id": 17, "name": "Water Filter Pitcher", "price": 25},
    18: {"id": 18, "name": "Glass Storage Containers", "price": 50},
    19: {"id": 19, "name": "Stainless Steel Cookware Set", "price": 300},
    20: {"id": 20, "name": "Non-Stick Frying Pan", "price": 40},
    21: {"id": 21, "name": "Bamboo Cutting Board", "price": 20},
    22: {"id": 22, "name": "Knife Set", "price": 95},
    23: {"id": 23, "name": "Spatula Set", "price": 15},
    24: {"id": 24, "name": "Digital Kitchen Scale", "price": 28},
    25: {"id": 25, "name": "Meat Thermometer", "price": 18},
    26: {"id": 26, "name": "Hand Mixer", "price": 40},
    27: {"id": 27, "name": "Rice Cooker", "price": 50},
    28: {"id": 28, "name": "Digital Air Fryer", "price": 130},
    29: {"id": 29, "name": "Dish Drying Rack", "price": 22},
    30: {"id": 30, "name": "Trash Can", "price": 30},
    31: {"id": 31, "name": "Floor Mop", "price": 25},
    32: {"id": 32, "name": "Broom and Dustpan Set", "price": 15},
    33: {"id": 33, "name": "Shower Curtain", "price": 20},
    34: {"id": 34, "name": "Bath Mat", "price": 18},
    35: {"id": 35, "name": "Towel Set", "price": 45},
    36: {"id": 36, "name": "Laundry Hamper", "price": 35},
    37: {"id": 37, "name": "Clothes Steamer", "price": 60},
    38: {"id": 38, "name": "Ironing Board", "price": 50},
    39: {"id": 39, "name": "Storage Baskets", "price": 40},
    40: {"id": 40, "name": "Set of 4 Pillows", "price": 60},
    41: {"id": 41, "name": "Duvet Cover Set", "price": 75},
    42: {"id": 42, "name": "Bed Sheets", "price": 50},
    43: {"id": 43, "name": "Throw Blanket", "price": 30},
    44: {"id": 44, "name": "Curtains", "price": 55},
    45: {"id": 45, "name": "Picture Frame Set", "price": 25},
    46: {"id": 46, "name": "Wall Mirror", "price": 70},
    47: {"id": 47, "name": "Dinnerware Set (4 person)", "price": 80},
    48: {"id": 48, "name": "Wine Glass Set", "price": 40},
    49: {"id": 49, "name": "Cocktail Shaker Set", "price": 35},
    50: {"id": 50, "name": "Insulated Water Bottle", "price": 20},
    51: {"id": 51, "name": "Lunch Box", "price": 15},
    52: {"id": 52, "name": "Herb Grinder", "price": 12},
    53: {"id": 53, "name": "Ice Cream Scoop", "price": 10},
    54: {"id": 54, "name": "Can Opener", "price": 10},
    55: {"id": 55, "name": "Corkscrew", "price": 15},
    56: {"id": 56, "name": "Bottle Opener", "price": 8},
    57: {"id": 57, "name": "Mixing Bowl Set", "price": 25},
    58: {"id": 58, "name": "Colander", "price": 18},
    59: {"id": 59, "name": "Serving Tray", "price": 30},
    60: {"id": 60, "name": "Salt and Pepper Shakers", "price": 15}
}

next_id = 3  # auto-increment counter


# -------------------------------
# GraphQL Schema Definitions
# -------------------------------
class Product(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    price = graphene.Int()


class Query(graphene.ObjectType):
    products = graphene.List(Product)
    product = graphene.Field(Product, id=graphene.Int(required=True))

    def resolve_products(self, info):
        return list(products_db.values())

    def resolve_product(self, info, id):
        return products_db.get(id)


# -------------------------------
# Mutations
# -------------------------------
class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Int(required=True)

    product = graphene.Field(lambda: Product)

    def mutate(self, info, name, price):
        global next_id
        product = {"id": next_id, "name": name, "price": price}
        products_db[next_id] = product
        next_id += 1
        return CreateProduct(product=product)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        price = graphene.Int()

    product = graphene.Field(lambda: Product)

    def mutate(self, info, id, name=None, price=None):
        product = products_db.get(id)
        if not product:
            raise Exception("Product not found")
        if name:
            product["name"] = name
        if price:
            product["price"] = price
        return UpdateProduct(product=product)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        if id in products_db:
            del products_db[id]
            return DeleteProduct(ok=True)
        return DeleteProduct(ok=False)


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()


# -------------------------------
# Flask App + GraphQL Endpoint
# -------------------------------
app = Flask(__name__)
schema = graphene.Schema(query=Query, mutation=Mutation)


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    result = schema.execute(
        data.get("query"),
        variables=data.get("variables")
    )
    response = {}
    if result.errors:
        response["errors"] = [str(e) for e in result.errors]
    if result.data:
        response["data"] = result.data
    return jsonify(response)


if __name__ == "__main__":
    # Run on all interfaces (0.0.0.0) so it works in LAN as well
    app.run(debug=True, host="0.0.0.0", port=7417)



'''
First, define the common headers used for all requests to avoid repetition.
powershell
# Define the common headers for GraphQL requests
$headers = @{ "Content-Type" = "application/json" }
$uri = "http://127.0.0.1:5000/graphql"
Use code with caution.

1. List all products's id, name, price
powershell
$body = @{
    query = "{ products { id name price } }"
} | ConvertTo-Json
$result = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
$result.data.products
Use code with caution.

2. List all products's name, price
powershell
$body = @{
    query = "{ products { name price } }"
} | ConvertTo-Json
$result = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
$result.data.products
Use code with caution.

3. Find a specific product
powershell
$body = @{
    query = "{ product(id:1) { id name } }"
} | ConvertTo-Json
$result = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
$result.data.product


4. Add a new product
powershell
$body = @{
    query = "mutation { createProduct(name: `"Tablet`", price: 700) { product { id name price } } }"
} | ConvertTo-Json
$result = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
$result.data.createProduct.product
Use code with caution.

5. Update a product
powershell
$body = @{
    query = "mutation { updateProduct(id: 1, name: `"Gaming Laptop`", price: 1200) { product { id name price } } }"
} | ConvertTo-Json
$result = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
$result.data.updateProduct.product
Use code with caution.

6. Delete a product
powershell
$body = @{
    query = "mutation { deleteProduct(id: 2) { ok } }"
} | ConvertTo-Json
$result = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
$result.data.deleteProduct
Use code with caution.
'''