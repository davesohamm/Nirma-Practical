# GREEDY ALGORITHM FOR MAKING CHANGE PROBLEM (LIMITED SUPPLY FOR EACH BILL AND COIN)

def make_change_with_limits(amount_in_dollars, denominations, names, available):
    amount = int(round(amount_in_dollars * 100))
    change = {}

    for i in range(len(denominations)):
        coin = denominations[i]
        max_available = available[i]
        needed = amount // coin
        use = min(needed, max_available)
        amount -= use * coin

        if use > 0:
            change[names[i]] = use

    return change, amount

names = ['100$ bill', '50$ bill', '20$ bill', '10$ bill', '5$ bill', '1$ bill',
         '25¢ coin', '10¢ coin', '5¢ coin', '1¢ coin']
denominations = [10000, 5000, 2000, 1000, 500, 100, 25, 10, 5, 1]

available = []
for n in names:
    available.append(int(input(f"How many {n}s do you have? ")))

amount_check = float(input("\nEnter the amount to make change for: "))
result, leftover = make_change_with_limits(amount_check, denominations, names, available)

print("\nChange given:")
for name, count in result.items():
    print(f"{name} : {count}")

if leftover > 0:
    print(f"\nCould not give full change. Remaining: {leftover/100:.2f} dollars. \n")
else:
    print("\nChange fully given. \n")
