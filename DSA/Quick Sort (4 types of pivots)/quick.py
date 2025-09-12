import time
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

sys.setrecursionlimit(200000)

# ---------------- Quick Sort Variants ---------------- #
def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

def partition(arr, low, high, pivot_type):
    if pivot_type == "first":
        pivot_index = low
    elif pivot_type == "last":
        pivot_index = high
    elif pivot_type == "random":
        pivot_index = random.randint(low, high)
    else:  # median of first, mid, last
        mid = (low + high)//2
        candidates = [(arr[low], low), (arr[mid], mid), (arr[high], high)]
        candidates.sort(key=lambda x: x[0])
        pivot_index = candidates[1][1]

    swap(arr, low, pivot_index)
    pivot = arr[low]
    i = low + 1
    j = high

    while True:
        while i <= j and arr[i] <= pivot:
            i += 1
        while i <= j and arr[j] >= pivot:
            j -= 1
        if i <= j:
            swap(arr, i, j)
        else:
            break

    swap(arr, low, j)
    return j

def quick_sort(arr, low, high, pivot_type):
    if low < high:
        pi = partition(arr, low, high, pivot_type)
        quick_sort(arr, low, pi - 1, pivot_type)
        quick_sort(arr, pi + 1, high, pivot_type)

# ---------------- Main Experiment ---------------- #
if __name__ == "__main__":
    sizes = [10000, 50000, 100000]
    pivot_types = ["first", "last", "random", "median"]
    LAST_K = 15

    # times dict: {pivot_type: {case: [times per n]}}
    times = {p: {"best": [], "average": [], "worst": []} for p in pivot_types}
    verification_records = []

    for n in sizes:
        print(f"\n=== Size {n} ===", flush=True)

        best = list(range(n))
        worst = list(range(n, 0, -1))
        avg = best.copy()
        random.shuffle(avg)

        cases = {"best": best, "average": avg, "worst": worst}

        for pivot_type in pivot_types:
            for case_name, arr in cases.items():
                arr_copy = arr.copy()
                original_last = arr_copy[-LAST_K:]
                start = time.time()
                quick_sort(arr_copy, 0, len(arr_copy)-1, pivot_type)
                end = time.time()
                t = end - start
                sorted_last = arr_copy[-LAST_K:]

                times[pivot_type][case_name].append(t)
                verification_records.append([pivot_type, case_name, n, t, original_last, sorted_last])

                print(f"[{pivot_type.title()} Pivot - {case_name.title()} | n={n}] Time: {t:.6f}s", flush=True)
                print(f"  Unsorted last {LAST_K}: {original_last}", flush=True)
                print(f"  Sorted   last {LAST_K}: {sorted_last}\n", flush=True)

    # Save verification log
    verify_df = pd.DataFrame(
        verification_records,
        columns=["Pivot Type", "Case", "Input Size", "Time Taken (s)", "Original Last 15", "Sorted Last 15"]
    )
    verify_df.to_csv("quicksort_verification.csv", index=False)
    print("Saved verification log to quicksort_verification.csv", flush=True)

    # ---------------- Plotting ---------------- #
    def plot_for_size(idx, n):
        # Build data: each pivot has 3 bars (best, avg, worst)
        labels = []
        values = []
        colors = []
        for pivot_type in pivot_types:
            for case in ["best", "average", "worst"]:
                labels.append(f"{pivot_type}\n{case}")
                values.append(times[pivot_type][case][idx])
                if case == "best":
                    colors.append("green")
                elif case == "average":
                    colors.append("blue")
                else:
                    colors.append("red")

        x = np.arange(len(labels))
        plt.figure(figsize=(12, 6))
        plt.bar(x, values, color=colors)
        plt.xticks(x, labels, rotation=45, ha='right')
        plt.ylabel("Time (seconds)")
        plt.title(f"QuickSort Variants Runtime Comparison ({n} elements)")
        plt.tight_layout()
        plt.savefig(f"quicksort_variants_{n}.png")
        plt.close()

    for idx, n in enumerate(sizes):
        plot_for_size(idx, n)

    print("Graphs saved as quicksort_variants_10000.png, quicksort_variants_50000.png, quicksort_variants_100000.png", flush=True)
