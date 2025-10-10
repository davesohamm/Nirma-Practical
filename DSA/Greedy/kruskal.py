def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    sorted_arr = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][0] <= right[j][0]:
            sorted_arr.append(left[i])
            i += 1
        else:
            sorted_arr.append(right[j])
            j += 1

    while i < len(left):
        sorted_arr.append(left[i])
        i += 1

    while j < len(right):
        sorted_arr.append(right[j])
        j += 1

    return sorted_arr

try:
    num_edges = int(input("Enter number of edges: "))
    if num_edges <= 0:
        print("Graph must have at least one edge.")
        exit()
except ValueError:
    print("Invalid input!")
    exit()

edges = []
vertices = set()

print("Enter each edge in format: u v weight (u and v can be any names)")
for i in range(num_edges):
    try:
        u, v, w = input(f"Edge {i+1}: ").split()
        if u == v:
            print("Self-loop. Edge skipped.")
            continue
        w = int(w)
        edges.append([w, u, v])
        vertices.add(u)
        vertices.add(v)
    except ValueError:
        print("Invalid input! Edge skipped.")

if not edges:
    print("No valid edges.")
    exit()

edges = merge_sort(edges)

parent = {v: v for v in vertices}

def find_parent(node):
    while parent[node] != node:
        node = parent[node]
    return node

mst = []
total_cost = 0

for w, u, v in edges:
    root_u = find_parent(u)
    root_v = find_parent(v)
    if root_u != root_v:
        mst.append([u, v, w])
        total_cost += w 
        parent[root_v] = root_u

if len(mst) != len(vertices) - 1:
    print("\nWarning: The graph is disconnected. MST includes only connected components.")

print("\nMinimum Spanning Tree:")
for u, v, w in mst:
    print(f"Edge {u} - {v}, Weight = {w}")

print(f"\nTotal Minimum Cost of MST = {total_cost}")
