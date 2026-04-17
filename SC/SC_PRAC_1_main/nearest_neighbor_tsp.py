import numpy as np
import matplotlib.pyplot as plt

distance_matrix = np.loadtxt('fri26_d.txt')
n = len(distance_matrix)

visited = [False]*n
path = [0]   # start from city 0
visited[0] = True

for _ in range(n-1):
    last = path[-1]
    nearest = None
    min_dist = float('inf')

    for j in range(n):
        if not visited[j] and distance_matrix[last][j] < min_dist:
            min_dist = distance_matrix[last][j]
            nearest = j

    path.append(nearest)
    visited[nearest] = True

# return to start
path.append(0)

print("NN Path:", path)

# Visualization
coords = np.random.rand(n, 2)

plt.figure()
for i in range(n):
    plt.scatter(coords[i][0], coords[i][1])

for i in range(len(path)-1):
    x1, y1 = coords[path[i]]
    x2, y2 = coords[path[i+1]]
    plt.plot([x1, x2], [y1, y2])

plt.title("Nearest Neighbor TSP")
plt.show()