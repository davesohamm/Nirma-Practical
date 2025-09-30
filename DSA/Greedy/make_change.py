# Greedy Algorithm for Make Change Problem - Unlimited Supply

def make_change(amount_dollars):
    amount = int(round(amount_dollars * 100))
    denominations = [
        10000,  # $100
        5000,   # $50
        2000,   # $20
        1000,   # $10
        500,    # $5
        100,    # $1
        25,     # 25¢
        10,     # 10¢
        5,      # 5¢
        1       # 1¢
    ]
    names = [
        "$100 bill",
        "$50 bill",
        "$20 bill",
        "$10 bill",
        "$5 bill",
        "$1 bill",
        "25¢ coin",
        "10¢ coin",
        "5¢ coin",
        "1¢ coin"
    ]

    change = {}
    for i in range(len(denominations)):
        coin = denominations[i]
        count = amount // coin
        amount %= coin
        if count > 0:
            change[names[i]] = count

    return change

amount_in_dollars = float(input("Enter the amount in dollars (e.g. 286.37): "))
result = make_change(amount_in_dollars)

print(f"\nChange for ${amount_in_dollars}:")
for denom, count in result.items():
    print(f"{denom} : {count}")
