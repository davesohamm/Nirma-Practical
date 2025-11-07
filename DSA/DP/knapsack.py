def knapsack_01_dp(W, weights, values):
    n = len(weights)
    B = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        wi = weights[i - 1]
        vi = values[i - 1]
        for w in range(W + 1):
            if wi > w:
                B[i][w] = B[i - 1][w]
            else:
                without_i = B[i - 1][w]
                with_i = vi + B[i - 1][w - wi]
                B[i][w] = max(without_i, with_i)

    max_value = B[n][W]

    print("\nDP TABLE")
    print("i  wi vi |", end="")
    for w in range(W + 1):
        print(f"{w:>5}", end="")
    print()

    print("-" * (7 + (W + 1) * 5))

    print(f"{0:>2}   -  - |", end="")
    for w in range(W + 1):
        print(f"{B[0][w]:>5}", end="")
    print()

    for i in range(1, n + 1):
        wi = weights[i - 1]
        vi = values[i - 1]
        print(f"{i:>2}  {wi:>3} {vi:>3} |", end="")
        for w in range(W + 1):
            print(f"{B[i][w]:>5}", end="")
        print()

    selected_items = []
    i, k = n, W
    while i > 0 and k >= 0:
        if B[i][k] != B[i - 1][k]:
            selected_items.append(i)
            k -= weights[i - 1]
        i -= 1
    
    selected_items.reverse()
    return max_value, selected_items

def read_int(msg):
    while True:
        try:
            x = int(input(msg).strip())
            if x < 0:
                print("Enter a non-negative integer.")
                continue
            return x
        except ValueError:
            print("Invalid input")

W = read_int("Enter the maximum capacity of the knapsack (W): ")
n = read_int("Enter the number of items: ")

if n == 0:
    print("No items available. Maximum value = 0")
    exit()

weights = []
values = []

for i in range(1, n+1):
    w = read_int(f"Enter weight of item {i}: ")
    v = read_int(f"Enter value of item {i}: ")
    weights.append(w)
    values.append(v)

max_value, items = knapsack_01_dp(W, weights, values)

print(f"\nMaximum value in knapsack = {max_value}")
if items:
    print("Items included:", ", ".join(map(str, items)))
else:
    print("No items were included.")