import random

goal = [1,2,3,4,5,6,7,8,0]

def heuristic(state):
    # number of misplaced tiles
    return sum([1 for i in range(9) if state[i] != goal[i]])

def get_neighbors(state):
    neighbors = []
    idx = state.index(0)

    moves = [-1,1,-3,3]  # left, right, up, down

    for move in moves:
        new_idx = idx + move
        if 0 <= new_idx < 9:
            new_state = state[:]
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
            neighbors.append(new_state)

    return neighbors

# random initial state
current = goal[:]
random.shuffle(current)

while True:
    neighbors = get_neighbors(current)
    next_state = min(neighbors, key=heuristic)

    if heuristic(next_state) >= heuristic(current):
        break

    current = next_state

print("Final State:", current)

# Visualization
for i in range(0,9,3):
    print(current[i:i+3])