def lcs_length_and_table(x, y):
    m, n = len(x), len(y)
    c = [[0] * (n + 1) for _ in range(m + 1)]
    b = [[''] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n+1):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = 'diag'
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                b[i][j] = 'up'
            else:
                c[i][j] = c[i][j - 1]
                b[i][j] = 'left'
    return c, b

def build_lcs(b,x,i,j):
    if i ==0 or j ==0:
        return ""
    if b[i][j] == 'diag':
        return build_lcs(b,x,i-1,j-1) + x[i-1]
    if b[i][j] == 'up':
        return build_lcs(b,x,i-1,j)
    return build_lcs(b,x,i,j-1)

x = input("Enter first string: ").strip()
y = input("Enter second string: ").strip()

if not x or not y:
    print("LCS length = 0")
    print("LCS = ''")

else:
    c, b = lcs_length_and_table(x, y)
    lcs = build_lcs(b, x, len(x), len(y))

    print("\nDP Table:")
    for row in c:
        print(" ".join(str(v) for v in row))

    print(f"\nLCS length = {len(lcs)}")
    print(f"LCS = '{lcs}'")