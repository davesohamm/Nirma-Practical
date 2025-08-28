import time
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

sys.setrecursionlimit(200000)

# ---------------- Sorting Algorithms ---------------- #
def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

def partition(arr, low, high):
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

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)


# ---------------- Main Experiment ---------------- #
if __name__ == "__main__":
    user_input_arr = [10000, 50000, 100000]
    LAST_K = 15

    selection_sort_best_times, selection_sort_avg_times, selection_sort_worst_times = [], [], []
    bubble_sort_best_times,    bubble_sort_avg_times,    bubble_sort_worst_times    = [], [], []
    insertion_sort_best_times, insertion_sort_avg_times, insertion_sort_worst_times = [], [], []
    quick_sort_best_times,     quick_sort_avg_times,     quick_sort_worst_times     = [], [], []

    verification_records = []

    for user_input in user_input_arr:

        # ---------- Selection Sort ----------
        arr = list(range(user_input)); random.shuffle(arr)
        original_last = arr[-LAST_K:]
        start = time.time(); selection_sort(arr); end = time.time()
        sorted_last = arr[-LAST_K:]; t = end - start
        selection_sort_avg_times.append(t)
        verification_records.append(["Selection", "Average", user_input, t, original_last, sorted_last])
        print(f"[Selection - Average | n={user_input}] Time: {t}s", flush=True)
        print(f"  Unsorted last {LAST_K}: {original_last}", flush=True)
        print(f"  Sorted   last {LAST_K}: {sorted_last}\n", flush=True)

        arr = list(range(user_input))
        original_last = arr[-LAST_K:]
        start = time.time(); selection_sort(arr); end = time.time()
        sorted_last = arr[-LAST_K:]; t = end - start
        selection_sort_best_times.append(t)
        verification_records.append(["Selection", "Best", user_input, t, original_last, sorted_last])
        print(f"[Selection - Best    | n={user_input}] Time: {t}s", flush=True)
        print(f"  Unsorted last {LAST_K}: {original_last}", flush=True)
        print(f"  Sorted   last {LAST_K}: {sorted_last}\n", flush=True)

        arr = list(range(user_input, 0, -1))
        original_last = arr[-LAST_K:]
        start = time.time(); selection_sort(arr); end = time.time()
        sorted_last = arr[-LAST_K:]; t = end - start
        selection_sort_worst_times.append(t)
        verification_records.append(["Selection", "Worst", user_input, t, original_last, sorted_last])
        print(f"[Selection - Worst   | n={user_input}] Time: {t}s", flush=True)
        print(f"  Unsorted last {LAST_K}: {original_last}", flush=True)
        print(f"  Sorted   last {LAST_K}: {sorted_last}\n", flush=True)

        # ---------- Bubble Sort ----------
        arr = list(range(user_input)); random.shuffle(arr)
        original_last = arr[-LAST_K:]
        start = time.time(); bubble_sort(arr); end = time.time()
        sorted_last = arr[-LAST_K:]; t = end - start
        bubble_sort_avg_times.append(t)
        verification_records.append(["Bubble", "Average", user_input, t, original_last, sorted_last])
        print(f"[Bubble    - Average | n={user_input}] Time: {t}s", flush=True)
        print(f"  Unsorted last {LAST_K}: {original_last}", flush=True)
        print(f"  Sorted   last {LAST_K}: {sorted_last}\n", flush=True)

        arr = list(range(user_input))
        original_last = arr[-LAST_K:]
        start = time.time(); bubble_sort(arr); end = time.time()
        sorted_last = arr[-LAST_K:]; t = end - start
        bubble_sort_best_times.append(t)
        verification_records.append(["Bubble", "Best", user_input, t, original_last, sorted_last])
        print(f"[Bubble    - Best    | n={user_input}] Time: {t}s", flush=True)
        print(f"  Unsorted last {LAST_K}: {original_last}", flush=True)
        print(f"  Sorted   last {LAST_K}: {sorted_last}\n", flush=True)

        arr = list(range(user_input, 0, -1))
        original_last = arr[-LAST_K:]
        start = time.time(); bubble_sort(arr); end = time.time()
        sorted_last = arr[-LAST_K:]; t = end - start
        bubble_sort_worst_times.append(t)
        verification_records.append(["Bubble", "Worst", user_input, t, original_last, sorted_last])
        print(f"[Bubble    - Worst   | n={user_input}] Time: {t}s", flush=True)
        print(f"  Unsorted last {LAST_K}: {original_last}", flush=True)
        print(f"  Sorted   last {LAST_K}: {sorted_last}\n", flush=True)

        # ---------- Insertion Sort ----------
        arr = list(range(user_input)); random.shuffle(arr)
        original_last = arr[-LAST_K:]
        start = time.time(); insertion_sort(arr); end = time.time()
        sorted_last = arr[-LAST_K:]; t = end - start
        insertion_sort_avg_times.append(t)
        verification_records.append(["Insertion", "Average", user_input, t, original_last, sorted_last])
        print(f"[Insertion - Average | n={user_input}] Time: {t}s", flush=True)
        print(f"  Unsorted last {LAST_K}: {original_last}", flush=True)
        print(f"  Sorted   last {LAST_K}: {sorted_last}\n", flush=True)

        arr = list(range(user_input))
        original_last = arr[-LAST_K:]
        start = time.time(); insertion_sort(arr); end = time.time()
        sorted_last = arr[-LAST_K:]; t = end - start
        insertion_sort_best_times.append(t)
        verification_records.append(["Insertion", "Best", user_input, t, original_last, sorted_last])
        print(f"[Insertion - Best    | n={user_input}] Time: {t}s", flush=True)
        print(f"  Unsorted last {LAST_K}: {original_last}", flush=True)
        print(f"  Sorted   last {LAST_K}: {sorted_last}\n", flush=True)

        arr = list(range(user_input, 0, -1))
        original_last = arr[-LAST_K:]
        start = time.time(); insertion_sort(arr); end = time.time()
        sorted_last = arr[-LAST_K:]; t = end - start
        insertion_sort_worst_times.append(t)
        verification_records.append(["Insertion", "Worst", user_input, t, original_last, sorted_last])
        print(f"[Insertion - Worst   | n={user_input}] Time: {t}s", flush=True)
        print(f"  Unsorted last {LAST_K}: {original_last}", flush=True)
        print(f"  Sorted   last {LAST_K}: {sorted_last}\n", flush=True)

        # ---------- Quick Sort ----------
        arr = list(range(user_input)); random.shuffle(arr)
        original_last = arr[-LAST_K:]
        start = time.time(); quick_sort(arr, 0, len(arr)-1); end = time.time()
        sorted_last = arr[-LAST_K:]; t = end - start
        quick_sort_avg_times.append(t)
        verification_records.append(["Quick", "Average", user_input, t, original_last, sorted_last])
        print(f"[Quick     - Average | n={user_input}] Time: {t}s", flush=True)
        print(f"  Unsorted last {LAST_K}: {original_last}", flush=True)
        print(f"  Sorted   last {LAST_K}: {sorted_last}\n", flush=True)

        arr = list(range(user_input))
        original_last = arr[-LAST_K:]
        start = time.time(); quick_sort(arr, 0, len(arr)-1); end = time.time()
        sorted_last = arr[-LAST_K:]; t = end - start
        quick_sort_best_times.append(t)
        verification_records.append(["Quick", "Best", user_input, t, original_last, sorted_last])
        print(f"[Quick     - Best    | n={user_input}] Time: {t}s", flush=True)
        print(f"  Unsorted last {LAST_K}: {original_last}", flush=True)
        print(f"  Sorted   last {LAST_K}: {sorted_last}\n", flush=True)

        arr = list(range(user_input, 0, -1))
        original_last = arr[-LAST_K:]
        start = time.time(); quick_sort(arr, 0, len(arr)-1); end = time.time()
        sorted_last = arr[-LAST_K:]; t = end - start
        quick_sort_worst_times.append(t)
        verification_records.append(["Quick", "Worst", user_input, t, original_last, sorted_last])
        print(f"[Quick     - Worst   | n={user_input}] Time: {t}s", flush=True)
        print(f"  Unsorted last {LAST_K}: {original_last}", flush=True)
        print(f"  Sorted   last {LAST_K}: {sorted_last}\n", flush=True)


    # ---------------- Save Verification CSV ---------------- #
    verify_df = pd.DataFrame(
        verification_records,
        columns=["Algorithm", "Case", "Input Size", "Time Taken (s)", "Original Last 15", "Sorted Last 15"]
    )
    verify_df.to_csv("sorting_verification.csv", index=False)
    print("Saved verification log to sorting_verification.csv", flush=True)

    # ---------------- Save Runtimes CSV---------------- #
    runtimes_df = pd.DataFrame({
        "Input Size": user_input_arr,
        "Selection Sort (Best)":   selection_sort_best_times,
        "Selection Sort (Average)":selection_sort_avg_times,
        "Selection Sort (Worst)":  selection_sort_worst_times,
        "Bubble Sort (Best)":      bubble_sort_best_times,
        "Bubble Sort (Average)":   bubble_sort_avg_times,
        "Bubble Sort (Worst)":     bubble_sort_worst_times,
        "Insertion Sort (Best)":   insertion_sort_best_times,
        "Insertion Sort (Average)":insertion_sort_avg_times,
        "Insertion Sort (Worst)":  insertion_sort_worst_times,
        "Quick Sort (Best)":       quick_sort_best_times,
        "Quick Sort (Average)":    quick_sort_avg_times,
        "Quick Sort (Worst)":      quick_sort_worst_times
    })
    runtimes_df.to_csv("sorting_runtimes.csv", index=False)
    print("Saved runtimes to sorting_runtimes.csv", flush=True)

    # ---------------- Plotting (3 graphs: 10k, 50k, 100k) ---------------- #
    def plot_for_input_index(idx, n_value):
        algorithms = ["Selection", "Bubble", "Insertion", "Quick"]
        x = np.arange(len(algorithms))
        width = 0.25

        best   = [selection_sort_best_times[idx],   bubble_sort_best_times[idx],   insertion_sort_best_times[idx],   quick_sort_best_times[idx]]
        avg    = [selection_sort_avg_times[idx],    bubble_sort_avg_times[idx],    insertion_sort_avg_times[idx],    quick_sort_avg_times[idx]]
        worst  = [selection_sort_worst_times[idx],  bubble_sort_worst_times[idx],  insertion_sort_worst_times[idx],  quick_sort_worst_times[idx]]

        plt.figure(figsize=(10, 6))
        plt.bar(x - width, best,  width, label="Best",   color="green")
        plt.bar(x,         avg,   width, label="Average",color="blue")
        plt.bar(x + width, worst, width, label="Worst",  color="red")

        plt.xticks(x, algorithms)
        plt.xlabel("Algorithms")
        plt.ylabel("Time (seconds)")
        plt.title(f"Sorting Runtime Comparison ({n_value} elements)")
        plt.legend(title="Case")
        plt.tight_layout()
        plt.savefig(f"runtime_comparison_{n_value}.png")
        plt.close()

    for idx, n in enumerate(user_input_arr):
        plot_for_input_index(idx, n)

    print("Graphs saved as runtime_comparison_10000.png, runtime_comparison_50000.png, runtime_comparison_100000.png", flush=True)
