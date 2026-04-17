import numpy as np
data = np.loadtxt('fri26_d.txt')
print("  ")
print("initial data from fri26_d.txt _ _ _ _ _")
print(" ")
print(data)

print("  ")
print("  ")
print("pheromone matrix _ _ _ _ _")
print("  ")
print(" ")
size = 26
random_matrix = np.random.rand(size, size)
pheromone_map = (random_matrix + random_matrix.T) / 2
print(pheromone_map)