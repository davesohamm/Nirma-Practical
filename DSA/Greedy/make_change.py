def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] >= right[j]:  # Descending
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def greedy_change(amount, coins):
    change = []
    for coin in coins:
        if amount >= coin:
            count = amount // coin
            amount %= coin
            change.extend([coin] * count)
    return change if amount == 0 else None

try:
    coins = list(map(int, input("Enter coin denominations (example: 1 5 2 100): ").split()))
    
    if not coins or any(c <= 0 for c in coins):
        print("Invalid denominations.")
    else:
        amount = int(input("Enter the amount you want change for: "))
        
        if amount < 0:
            print("Amount cannot be negative.")
        elif amount == 0:
            print("No change needed.")
        else:
            coins = merge_sort(coins)
            
            result = greedy_change(amount, coins)
            print("Change:", *result) if result else print("Change is not possible.")
except ValueError:
    print("Invalid input.")
