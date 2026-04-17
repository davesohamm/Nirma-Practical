import itertools
import matplotlib.pyplot as plt
import numpy as np

# Load distance matrix from file
distance_matrix = np.loadtxt('fri26_d.txt')

n = len(distance_matrix)
cities = list(range(n))

def calculate_cost(path):
    cost = 0
    for i in range(len(path) - 1):
        cost += distance_matrix[path[i]][path[i+1]]
    cost += distance_matrix[path[-1]][path[0]]  # return to start
    return cost

best_path = None
min_cost = float('inf')

# Try all permutations (fix first city to reduce computation)
for perm in itertools.permutations(cities[1:]):
    path = [0] + list(perm)
    cost = calculate_cost(path)

    if cost < min_cost:
        min_cost = cost
        best_path = path

print("Best Path:", best_path)
print("Minimum Cost:", min_cost)

# Visualization (random positions)
coords = np.random.rand(n, 2)

plt.figure()
for i in range(n):
    plt.scatter(coords[i][0], coords[i][1])

for i in range(len(best_path)):
    x1, y1 = coords[best_path[i]]
    x2, y2 = coords[best_path[(i+1) % n]]
    plt.plot([x1, x2], [y1, y2])

plt.title("Brute Force TSP Path")
plt.show()