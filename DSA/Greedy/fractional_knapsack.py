def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][0] >= right[j][0]:  # Descending
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def fractional_knapsack():
    n = int(input("Enter number of items: "))
    if n <= 0:
        print("No items.")
        return

    values = []
    weights = []

    for i in range(n):
        v = float(input(f"Enter value of item {i+1}: "))
        w = float(input(f"Enter weight of item {i+1}: "))

        if v < 0 or w <= 0:
            print(f"Skipping item {i+1} !! BECAUSE IT'S - invalid input.")
            continue

        values.append(v)
        weights.append(w)

    if not values:
        print("No valid items available.")
        return

    capacity = float(input("Enter knapsack capacity: "))
    if capacity <= 0:
        print("Knapsack capacity must be greater than zero.")
        return
    
    ratio_list = []
    for i in range(len(values)):
        ratio = values[i] / weights[i]
        ratio_list.append((ratio, values[i], weights[i]))

    ratio_list = merge_sort(ratio_list)

    total_value = 0
    remaining = capacity

    print("\nSelected items based on best v/w ratio")
    for ratio, value, weight in ratio_list:
        if remaining == 0:
            break

        if weight <= remaining:
            total_value += value
            remaining -= weight
            taken_value = value
            taken_weight = weight
        else:
            fraction = remaining / weight
            total_value += value * fraction
            taken_value = value * fraction
            taken_weight = remaining
            remaining = 0

        print(f"Taking Value: {round(taken_value,2)}, Weight: {round(taken_weight,2)}, Ratio: {round(ratio,2)}")

    print("\n Maximum value that can be obtained =", round(total_value, 2))

fractional_knapsack()