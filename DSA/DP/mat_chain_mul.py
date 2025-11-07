import sys

def get_user_dimensions():
    print("Enter the matrix dimensions as a space-separated list.")
    print("If you have n matrices A1, A2, ..., An, then enter n+1 numbers.")
    print("Example: For A1(10x100), A2(100x5), A3(5x50), enter: 10 100 5 50")
    print()

    while True:
        user_input = input("Enter dimensions: ").strip()
        try:
            dims = [int(x) for x in user_input.split()]
            if len(dims) < 3:
                print("\nYou must enter at least 3 numbers (for 2 matrices). Try again.\n")
            else:
                return dims
        except ValueError:
            print("\nInvalid input.\n")

def matrix_chain_order(P):
    n = len(P) - 1
    M = [[0] * (n + 1) for _ in range(n + 1)]
    S = [[0] * (n + 1) for _ in range(n + 1)]

    for L in range(2, n + 1):
        for i in range(1, n - L + 2):
            j = i + L - 1
            M[i][j] = sys.maxsize

            for k in range(i, j):
                cost = M[i][k] + M[k + 1][j] + (P[i - 1] * P[k] * P[j])
                
                if cost < M[i][j]:
                    M[i][j] = cost
                    S[i][j] = k
    return M, S

def print_table(table, title):
    n = len(table) - 1
    print(f"\n{title} (1-indexed)")

    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            if j < i:
                row.append("   -")
            else:
                row.append(f"{table[i][j]:5}")
        print(f"Row {i}: " + " ".join(row))
    
def optimal_parenthesization(S, i, j):
    if i == j:
        return f"A{i}"
    k = S[i][j]
    left = optimal_parenthesization(S, i, k)
    right = optimal_parenthesization(S, k + 1, j)
    return f"({left} x {right})"

if __name__ == "__main__":
    P = get_user_dimensions()
    n = len(P) - 1

    if n < 2:
        print("At least two matrices are required for multiplication.")
        sys.exit()

    M, S = matrix_chain_order(P)
    min_cost = M[1][n]

    print("\n__")
    print(f"Number of Matrices: {n}")
    print(f"Minimum Scalar Multiplications Required: {min_cost}")
    print("\n__")

    print_table(M, "Cost Matrix (M)")
    print_table(S, "Split Matrix (S)")

    print("\n__")
    print("Optimal Parenthesis (Best Multiplication Order):")
    print(optimal_parenthesization(S, 1, n))
    print("\n__")