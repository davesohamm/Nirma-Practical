import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import heapq

# ---------------- Internal Merge Sort ---------------- #
def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    L = arr[left:mid+1]
    R = arr[mid+1:right+1]

    i = j = 0
    k = left

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def internal_merge_sort(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        internal_merge_sort(arr, left, mid)
        internal_merge_sort(arr, mid+1, right)
        merge(arr, left, mid, right)

# ---------------- K-way Merge (File-based) ---------------- #
def k_way_merge(temp_file_paths, output_file_path):

    input_files = []
    heap = []
    readers = []

    try:
        # Open each temporary file and initialize the heap
        for i, file_path in enumerate(temp_file_paths):
            f = open(file_path, 'r')
            readers.append(csv.reader(f))
            try:
                # Read the first element and push to heap (convert to int)
                first_element = next(readers[-1])
                if first_element:
                    heapq.heappush(heap, (int(first_element[0]), i))
            except StopIteration:
                # Handle empty files
                pass
            input_files.append(f)

        # Open the output file
        with open(output_file_path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)

            # Merge using the min-heap
            while heap:
                smallest_element, file_index = heapq.heappop(heap)
                writer.writerow([smallest_element])

                # Read the next element from the file the smallest came from
                try:
                    next_element = next(readers[file_index])
                    if next_element:
                        heapq.heappush(heap, (int(next_element[0]), file_index))
                except StopIteration:
                    # File is exhausted
                    pass

    except Exception as e:
        print(f"An error occurred during k-way merge: {e}")
    finally:
        # Close all input files
        for f in input_files:
            f.close()

# ---------------- External Merge Sort (File-based) ---------------- #
def external_merge_sort(arr, output_file_path, chunk_size=1000):
    temp_files = []
    for i in range(0, len(arr), chunk_size):
        chunk = arr[i:i+chunk_size]
        internal_merge_sort(chunk, 0, len(chunk)-1)

        file_path = f"temp_chunk_{i // chunk_size}.csv"
        pd.DataFrame(chunk).to_csv(file_path, index=False, header=False)
        temp_files.append(file_path)

    k_way_merge(temp_files, output_file_path)
    return output_file_path

# ---------------- Main Experiment ---------------- #
def run_experiment():
    sizes = [10000, 50000, 100000]
    chunk_size = 1000
    cases = {
        "Best": lambda n: list(range(n)),
        "Average": lambda n: random.sample(range(n), n),
        "Worst": lambda n: list(range(n, 0, -1))
    }

    results = []
    last_15_elements_data = []

    for size in sizes:
        print(f"\n{'='*20} Input Size: {size} {'='*20}")
        for case_name, case_gen in cases.items():
            arr = case_gen(size)
            arr_copy1 = arr[:]  # For internal
            arr_copy2 = arr[:] # For external

            original_last_15 = arr[-15:] if len(arr) >= 15 else arr
            print(f"\nCase: {case_name}")
            print(f"  Original last 15 elements: {original_last_15}")
            last_15_elements_data.append({
                "Algorithm": "Original",
                "Input Size": size,
                "Case": case_name,
                "Last 15 Elements": original_last_15
            })

            print(f"  Internal Merge Sort:")
            start = time.time()
            internal_merge_sort(arr_copy1, 0, len(arr_copy1)-1)
            end = time.time()
            internal_time = end - start
            print(f"    Time: {internal_time:.6f} sec")
            results.append(["Internal Merge Sort", size, case_name, None, internal_time])

            internal_sorted_last_15 = arr_copy1[-15:] if len(arr_copy1) >= 15 else arr_copy1
            print(f"    Sorted last 15 elements: {internal_sorted_last_15}")
            last_15_elements_data.append({
                "Algorithm": "Internal Merge Sort",
                "Input Size": size,
                "Case": case_name,
                "Last 15 Elements": internal_sorted_last_15
            })

            print(f"  External Merge Sort:")
            output_file = f"external_sorted_{size}_{case_name}_chunk_{chunk_size}.csv"
            start = time.time()
            external_merge_sort(arr_copy2, output_file, chunk_size=chunk_size)
            end = time.time()
            external_time = end - start
            print(f"    Time: {external_time:.6f} sec")
            results.append(["External Merge Sort", size, case_name, chunk_size, external_time])

            try:
                external_sorted_df = pd.read_csv(output_file, header=None)
                external_sorted_arr = external_sorted_df[0].tolist()
                external_sorted_last_15 = external_sorted_arr[-15:] if len(external_sorted_arr) >= 15 else external_sorted_arr
                print(f"    Sorted last 15 elements from file: {external_sorted_last_15}")
                last_15_elements_data.append({
                    "Algorithm": "External Merge Sort",
                    "Input Size": size,
                    "Case": case_name,
                    "Last 15 Elements": external_sorted_last_15
                })
            except Exception as e:
                print(f"Error reading external sort output file {output_file}: {e}")

    df_runtimes = pd.DataFrame(results, columns=["Algorithm", "Input Size", "Case", "Chunk Size", "Runtime"])
    df_runtimes.to_csv("merge_sort_fixed_chunk_results.csv", index=False)
    print("\nRuntime results saved to merge_sort_fixed_chunk_results.csv")

    df_last_15 = pd.DataFrame(last_15_elements_data)
    df_last_15.to_csv("merge_sort_last_15_elements.csv", index=False)
    print("Last 15 elements data saved to merge_sort_last_15_elements.csv")

    plot_graphs(df_runtimes)


def plot_graphs(df):
    sizes = df["Input Size"].unique()
    cases = df["Case"].unique()
    chunk_size_series = df["Chunk Size"].dropna().unique()
    chunk_size = chunk_size_series[0] if chunk_size_series.size > 0 else 'N/A'
    case_colors = {"Best": "green", "Average": "blue", "Worst": "red"}

    for size in sizes:
        plt.figure(figsize=(12, 7))
        subset = df[df["Input Size"] == size]

        num_algorithms = 2
        num_cases = len(cases)
        group_width = num_cases * 0.8
        bar_width = group_width / num_cases
        gap_between_algorithms = 0.4

        internal_group_center = num_cases * bar_width / 2
        external_group_center = internal_group_center + group_width + gap_between_algorithms

        internal_bar_positions = np.linspace(internal_group_center - group_width / 2 + bar_width / 2,
                                             internal_group_center + group_width / 2 - bar_width / 2,
                                             num_cases)
        external_bar_positions = np.linspace(external_group_center - group_width / 2 + bar_width / 2,
                                             external_group_center + group_width / 2 - bar_width / 2,
                                             num_cases)


        internal_runtimes = [subset[(subset["Algorithm"] == "Internal Merge Sort") & (subset["Case"] == case)]["Runtime"].iloc[0] for case in cases]
        external_runtimes = [subset[(subset["Algorithm"] == "External Merge Sort") & (subset["Case"] == case)]["Runtime"].iloc[0] for case in cases]

        plt.bar(internal_bar_positions, internal_runtimes, bar_width, color=[case_colors[case] for case in cases])
        plt.bar(external_bar_positions, external_runtimes, bar_width, color=[case_colors[case] for case in cases])

        plt.ylabel("Runtime (seconds)")
        plt.title(f"Merge Sort Performance - Input Size: {size}")

        all_bar_positions = np.concatenate([internal_bar_positions, external_bar_positions])
        x_labels = [f"Internal\n{case}" for case in cases] + [f"External\n{case}\n(Chunk {chunk_size})" for case in cases]
        plt.xticks(all_bar_positions, x_labels)

        case_legend_handles = [plt.Rectangle((0,0),1,1, color=case_colors[case]) for case in cases]
        plt.legend(case_legend_handles, cases, title="Case Type", bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        plt.savefig(f"merge_sort_performance_size_{size}_chunk_{chunk_size}.png")
        plt.show()

if __name__ == "__main__":
    run_experiment()