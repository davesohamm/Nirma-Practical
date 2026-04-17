"""Generate synthetic car_details.csv for pipeline testing."""
import os
import random
import csv

random.seed(42)

BRANDS = {
    "Maruti": ["Swift", "Alto", "Baleno", "Ciaz", "Wagon R", "Dzire", "Vitara"],
    "Hyundai": ["i20", "Creta", "Venue", "Verna", "Santro", "Grand"],
    "Honda": ["City", "Amaze", "Jazz", "WRV", "Civic"],
    "Toyota": ["Innova", "Fortuner", "Etios", "Corolla", "Camry"],
    "Tata": ["Nexon", "Harrier", "Safari", "Tiago", "Altroz"],
    "Ford": ["EcoSport", "Figo", "Aspire", "Endeavour"],
    "Mahindra": ["Scorpio", "XUV500", "Bolero", "XUV300", "Thar"],
    "Volkswagen": ["Polo", "Vento", "Tiguan", "Passat"],
    "Renault": ["Kwid", "Duster", "Triber", "Kiger"],
    "Kia": ["Seltos", "Sonet", "Carnival"],
    "BMW": ["3 Series", "5 Series", "X1", "X3"],
    "Mercedes-Benz": ["C-Class", "E-Class", "GLA", "GLC"],
    "Audi": ["A4", "A6", "Q3", "Q5"],
    "Skoda": ["Rapid", "Superb", "Octavia", "Kushaq"],
    "Chevrolet": ["Beat", "Cruze", "Spark", "Enjoy"],
}

FUEL_TYPES = ["Petrol", "Diesel", "CNG", "LPG"]
SELLER_TYPES = ["Individual", "Dealer", "Trustmark Dealer"]
TRANSMISSIONS = ["Manual", "Automatic"]
OWNERS = ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner"]

ROWS = 5000

output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "car_details.csv")

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "year", "selling_price", "km_driven", "fuel",
                      "seller_type", "transmission", "owner", "mileage",
                      "engine", "max_power", "torque", "seats"])

    for _ in range(ROWS):
        brand = random.choice(list(BRANDS.keys()))
        model = random.choice(BRANDS[brand])
        name = f"{brand} {model}"

        year = random.randint(2000, 2024)
        car_age = 2025 - year

        # Price depends on brand tier and age
        if brand in ("BMW", "Mercedes-Benz", "Audi"):
            base_price = random.randint(800000, 5000000)
        elif brand in ("Toyota", "Kia"):
            base_price = random.randint(400000, 2500000)
        else:
            base_price = random.randint(100000, 1500000)

        depreciation = max(0.2, 1 - car_age * 0.07)
        selling_price = int(base_price * depreciation * random.uniform(0.8, 1.2))
        selling_price = max(30000, selling_price)

        km_driven = random.randint(5000, 200000) + car_age * random.randint(3000, 12000)
        km_driven = min(km_driven, 400000)

        fuel = random.choices(FUEL_TYPES, weights=[50, 35, 10, 5])[0]
        seller = random.choices(SELLER_TYPES, weights=[50, 35, 15])[0]
        transmission = random.choices(TRANSMISSIONS, weights=[65, 35])[0]
        owner = random.choices(OWNERS, weights=[50, 30, 15, 5])[0]

        mileage = round(random.uniform(8, 30), 2)
        mileage_str = f"{mileage} kmpl" if fuel != "CNG" else f"{mileage} km/kg"

        engine = random.choice([799, 998, 1197, 1248, 1497, 1498, 1999, 2179, 2694, 2993])
        engine_str = f"{engine} CC"

        max_power = round(random.uniform(40, 200), 2)
        power_str = f"{max_power} bhp"

        torque_val = round(random.uniform(70, 400), 1)
        torque_str = f"{torque_val} Nm"

        seats = random.choices([4, 5, 6, 7, 8], weights=[5, 60, 10, 20, 5])[0]

        writer.writerow([name, year, selling_price, km_driven, fuel, seller,
                          transmission, owner, mileage_str, engine_str,
                          power_str, torque_str, seats])

print(f"Generated {ROWS} rows at {output_path}")
