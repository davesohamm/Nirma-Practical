import time
import random
import matplotlib.pyplot as plt
import pandas as pd
import os

# ---------------- Sorting Algorithms ---------------- #
def selection_sort(arr):
    n = len(arr)
    for i in range(n-1):
        min_index = i
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        swapped = False
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
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

# ---------------- Main Experiment ---------------- #
if __name__ == "__main__":
    user_input_arr = [10000, 50000, 100000]
    num_runs = 1  # Increase this for higher accuracy

    all_run_results = []
    verification_records = []  

    for run in range(num_runs):
        selection_sort_best_times, selection_sort_avg_times, selection_sort_worst_times = [], [], []
        bubble_sort_best_times, bubble_sort_avg_times, bubble_sort_worst_times = [], [], []
        insertion_sort_best_times, insertion_sort_avg_times, insertion_sort_worst_times = [], [], []

        for user_input in user_input_arr:
            # ---------- Selection Sort ----------
            arr = list(range(user_input))
            random.shuffle(arr)
            original_last5 = arr[-5:]
            start = time.time(); selection_sort(arr); end = time.time()
            sorted_last5 = arr[-5:]
            selection_sort_avg_times.append(end - start)
            verification_records.append(["Selection", "Average", user_input, original_last5, sorted_last5])

            arr = list(range(user_input))
            original_last5 = arr[-5:]
            start = time.time(); selection_sort(arr); end = time.time()
            sorted_last5 = arr[-5:]
            selection_sort_best_times.append(end - start)
            verification_records.append(["Selection", "Best", user_input, original_last5, sorted_last5])

            arr = list(range(user_input, 0, -1))
            original_last5 = arr[-5:]
            start = time.time(); selection_sort(arr); end = time.time()
            sorted_last5 = arr[-5:]
            selection_sort_worst_times.append(end - start)
            verification_records.append(["Selection", "Worst", user_input, original_last5, sorted_last5])

            # ---------- Bubble Sort ----------
            arr = list(range(user_input))
            random.shuffle(arr)
            original_last5 = arr[-5:]
            start = time.time(); bubble_sort(arr); end = time.time()
            sorted_last5 = arr[-5:]
            bubble_sort_avg_times.append(end - start)
            verification_records.append(["Bubble", "Average", user_input, original_last5, sorted_last5])

            arr = list(range(user_input))
            original_last5 = arr[-5:]
            start = time.time(); bubble_sort(arr); end = time.time()
            sorted_last5 = arr[-5:]
            bubble_sort_best_times.append(end - start)
            verification_records.append(["Bubble", "Best", user_input, original_last5, sorted_last5])

            arr = list(range(user_input, 0, -1))
            original_last5 = arr[-5:]
            start = time.time(); bubble_sort(arr); end = time.time()
            sorted_last5 = arr[-5:]
            bubble_sort_worst_times.append(end - start)
            verification_records.append(["Bubble", "Worst", user_input, original_last5, sorted_last5])

            # ---------- Insertion Sort ----------
            arr = list(range(user_input))
            random.shuffle(arr)
            original_last5 = arr[-5:]
            start = time.time(); insertion_sort(arr); end = time.time()
            sorted_last5 = arr[-5:]
            insertion_sort_avg_times.append(end - start)
            verification_records.append(["Insertion", "Average", user_input, original_last5, sorted_last5])

            arr = list(range(user_input))
            original_last5 = arr[-5:]
            start = time.time(); insertion_sort(arr); end = time.time()
            sorted_last5 = arr[-5:]
            insertion_sort_best_times.append(end - start)
            verification_records.append(["Insertion", "Best", user_input, original_last5, sorted_last5])

            arr = list(range(user_input, -1, -1))
            original_last5 = arr[-5:]
            start = time.time(); insertion_sort(arr); end = time.time()
            sorted_last5 = arr[-5:]
            insertion_sort_worst_times.append(end - start)
            verification_records.append(["Insertion", "Worst", user_input, original_last5, sorted_last5])

        run_data = {
            'Input Size': user_input_arr,
            'Selection Sort (Best)': selection_sort_best_times,
            'Selection Sort (Average)': selection_sort_avg_times,
            'Selection Sort (Worst)': selection_sort_worst_times,
            'Bubble Sort (Best)': bubble_sort_best_times,
            'Bubble Sort (Average)': bubble_sort_avg_times,
            'Bubble Sort (Worst)': bubble_sort_worst_times,
            'Insertion Sort (Best)': insertion_sort_best_times,
            'Insertion Sort (Average)': insertion_sort_avg_times,
            'Insertion Sort (Worst)': insertion_sort_worst_times
        }
        run_df = pd.DataFrame(run_data)
        all_run_results.append(run_df)

    # Concatenate all runs
    combined_df = pd.concat(all_run_results, ignore_index=True)
    combined_df.to_csv("sorting_runtimes_raw.csv", index=False)

    # Compute average runtimes across runs
    avg_df = combined_df.groupby("Input Size").mean().reset_index()
    avg_df.to_csv("sorting_runtimes_average.csv", index=False)

    # Save verification file
    verify_df = pd.DataFrame(verification_records,
                             columns=["Algorithm", "Case", "Input Size", "Original Last 5", "Sorted Last 5"])
    verify_df.to_csv("sorting_verification.csv", index=False)

    print("Saved raw runtimes to sorting_runtimes_raw.csv")
    print("Saved average runtimes to sorting_runtimes_average.csv")
    print("Saved verification log to sorting_verification.csv")

    # ---------------- Plotting ---------------- #
    def plot_algorithm(algorithm_name, avg_df):
        cases = ["Best", "Average", "Worst"]
        input_sizes = avg_df["Input Size"].tolist()

        times = []
        for case in cases:
            col = f"{algorithm_name} Sort ({case})"
            times.append(avg_df[col].tolist())

        plot_df = pd.DataFrame(times, index=cases, columns=input_sizes)
        plot_df.T.plot(kind="bar", figsize=(10,6))
        plt.title(f"{algorithm_name} Sort Runtime Comparison")
        plt.xlabel("Input Size")
        plt.ylabel("Time (seconds)")
        plt.legend(title="Case")
        plt.tight_layout()
        plt.savefig(f"{algorithm_name.lower()}_sort_times.png")
        plt.close()

    plot_algorithm("Selection", avg_df)
    plot_algorithm("Bubble", avg_df)
    plot_algorithm("Insertion", avg_df)

    print("Graphs saved as selection_sort_times.png, bubble_sort_times.png, insertion_sort_times.png")
