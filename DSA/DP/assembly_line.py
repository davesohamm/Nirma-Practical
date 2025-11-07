def assembly_line_scheduling(n, a, t, e, x):
    dp = [[0 for _ in range(n)] for _ in range(2)]
    dp[0][0] = e[0] + a[0][0]
    dp[1][0] = e[1] + a[1][0]
    for i in range(1, n):
        dp[0][i] = min(
            dp[0][i - 1] + a[0][i],
            dp[1][i - 1] + t[1][i - 1] + a[0][i]
        )

        dp[1][i] = min(
            dp[1][i - 1] + a[1][i],
            dp[0][i - 1] + t[0][i - 1] + a[1][i]
        )
    final_time = min(dp[0][n - 1] + x[0], dp[1][n - 1] + x[1])
    print("DP Table:")
    for i in range(2):
        print("Line", i + 1, ":", dp[i])
    print("\nFinal Minimum Time:", final_time)

try:
    n = int(input("Enter number of stations: "))
    if n <= 0:
        raise ValueError("Number of stations must be positive.")

    a = [[], []]
    print("Enter processing times for Line 1:")
    a[0] = list(map(int, input().split()))
    print("Enter processing times for Line 2:")
    a[1] = list(map(int, input().split()))
        # Validate input sizes
    if len(a[0]) != n or len(a[1]) != n:
        raise ValueError("Processing times must match number of stations.")

    t = [[], []]
    if n > 1:
        print("Enter transfer times from Line 1 to Line 2:")
        t[0] = list(map(int, input().split()))
        print("Enter transfer times from Line 2 to Line 1:")
        t[1] = list(map(int, input().split()))
        
        if len(t[0]) != n - 1 or len(t[1]) != n - 1:
            raise ValueError("Transfer times must have n-1 values each.")
    else:
        t = [[0], [0]]


    e = list(map(int, input("Enter entry times for both lines: ").split()))
    x = list(map(int, input("Enter exit times for both lines: ").split()))

    if len(e) != 2 or len(x) != 2:
        raise ValueError("Entry and exit times must each have 2 values.")

    assembly_line_scheduling(n, a, t, e, x)

except ValueError as ve:
    print(f"Input Error: {ve}")
except Exception as e:
    print(f"Unexpected Error: {e}") 