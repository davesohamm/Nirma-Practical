from itertools import permutations

goal = (1,2,3,4,5,6,7,8,0)

def is_goal(state):
    return state == goal

# Generate all possible states (brute force idea)
for perm in permutations(range(9)):
    if is_goal(perm):
        print("Goal Found:", perm)
        break

# Visualization (print grid)
def print_grid(state):
    for i in range(0,9,3):
        print(state[i:i+3])
    print()

print_grid(goal)