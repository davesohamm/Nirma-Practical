# BEFORE RUNNING THE PROGRAM - pip install plotext
import time
import random
import plotext as plt

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
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        insert_index = i
        current_value = arr.pop(i)
        for j in range(i-1, -1, -1):
            if arr[j] > current_value:
                insert_index = j
        arr.insert(insert_index, current_value)


if __name__ == "__main__":
    user_input_string = input("Enter input size:")
    user_input = int(user_input_string)


# SELECTION SORT EXECUTION ----------
    

    avgcase_arr_selection_sort = random.sample(range(100000), user_input)
    # print(f"Original Array: {avgcase_arr_selection_sort}")
    avgcase_start_time_selection_sort = time.time()
    selection_sort(avgcase_arr_selection_sort)
    avgcase_end_time_selection_sort = time.time()
    # print(f"Sorted Array: {avgcase_arr_selection_sort}")
    avgcase_time_taken_selection_sort = avgcase_end_time_selection_sort - avgcase_start_time_selection_sort
    print(f"AVG CASE execution time for SELECTION SORT: {avgcase_time_taken_selection_sort}")
    
    bestcase_arr_selection_sort = []
    for i in range(0, user_input):
        bestcase_arr_selection_sort.append(i)
    # print(f"Original Array: {bestcase_arr_selection_sort}")
    bestcase_start_time_selection_sort = time.time()
    selection_sort(bestcase_arr_selection_sort)
    bestcase_end_time_selection_sort = time.time()
    # print(f"Sorted Array: {bestcase_arr_selection_sort}")
    bestcase_time_taken_selection_sort = bestcase_end_time_selection_sort - bestcase_start_time_selection_sort
    print(f"BEST CASE execution time for SELECTION SORT: {bestcase_time_taken_selection_sort}")
    
    worstcase_arr_selection_sort = []
    for j in range(user_input, 0, -1):
        worstcase_arr_selection_sort.append(j)
    # print(f"Original Array: {worstcase_arr_selection_sort}")
    worstcase_start_time_selection_sort = time.time()
    selection_sort(worstcase_arr_selection_sort)
    worstcase_end_time_selection_sort = time.time()
    # print(f"Sorted Array: {worstcase_arr}")
    worstcase_time_taken_selection_sort = worstcase_end_time_selection_sort - worstcase_start_time_selection_sort
    print(f"WORST CASE execution time for SELECTION SORT: {worstcase_time_taken_selection_sort}")

    
    labels = ["BEST", "AVG", "WORST"]
    plt.bar(labels, [bestcase_time_taken_selection_sort, avgcase_time_taken_selection_sort, worstcase_time_taken_selection_sort])
    plt.title("Selection Sort Execution Time")
    plt.xlabel("Type of cases")
    plt.ylabel("Execution time")
    plt.plotsize(50, 30)
    plt.show()


# BUBBLE SORT EXECUTION ----------


    avgcase_arr_bubble_sort = random.sample(range(100000), user_input)
    # print(f"Original Array: {avgcase_arr_bubble_sort}")
    avgcase_start_time_bubble_sort = time.time()
    bubble_sort(avgcase_arr_bubble_sort)
    avgcase_end_time_bubble_sort = time.time()
    # print(f"Sorted Array: {avgcase_arr_bubble_sort}")
    avgcase_time_taken_bubble_sort = avgcase_end_time_bubble_sort - avgcase_start_time_bubble_sort
    print(f"AVG CASE execution time for BUBBLE SORT: {avgcase_time_taken_bubble_sort}")

    bestcase_arr_bubble_sort = []
    for i in range(0, user_input):
        bestcase_arr_bubble_sort.append(i)
    # print(f"Original Array: {bestcase_arr_bubble_sort}")
    bestcase_start_time_bubble_sort = time.time()
    bubble_sort(bestcase_arr_bubble_sort)
    # print(f"Sorted Array: {bestcase_arr_bubble_sort}")
    bestcase_end_time_bubble_sort = time.time()
    bestcase_time_taken_bubble_sort = bestcase_end_time_bubble_sort - bestcase_start_time_bubble_sort
    print(f"BEST CASE execution time for BUBBLE SORT: {bestcase_time_taken_bubble_sort}")

    worstcase_arr_bubble_sort = []
    for j in range(user_input, 0, -1):
        worstcase_arr_bubble_sort.append(j)
    # print(f"Original Array: {worstcase_arr_bubble_sort}")
    worstcase_start_time_bubble_sort = time.time()
    bubble_sort(worstcase_arr_bubble_sort)
    worstcase_end_time_bubble_sort = time.time()
    # print(f"Sorted Array: {worstcase_arr_bubble_sort}")
    worstcase_time_taken_bubble_sort = worstcase_end_time_bubble_sort - worstcase_start_time_bubble_sort
    print(f"WORST CASE execution time for BUBBLE SORT: {worstcase_time_taken_bubble_sort}")

    plt.clf()
    labels = ["BEST", "AVG", "WORST"]
    plt.bar(labels, [bestcase_time_taken_bubble_sort, avgcase_time_taken_bubble_sort, worstcase_time_taken_bubble_sort])
    plt.title("Bubble Sort Execution Time")
    plt.xlabel("Type of cases")
    plt.ylabel("Execution time")
    plt.plotsize(50, 30)
    plt.show()


# INSERTION SORT EXECUTION ---------- 


    avgcase_arr_insertion_sort = random.sample(range(100000), user_input)
    # print(f"Original Array: {avgcase_arr_insertion_sort}")
    avgcase_start_time_insertion_sort = time.time()
    insertion_sort(avgcase_arr_insertion_sort)
    # print(f"Sorted Array: {avgcase_arr_insertion_sort}")
    avgcase_end_time_insertion_sort = time.time()
    avgcase_time_taken_insertion_sort = avgcase_end_time_insertion_sort - avgcase_start_time_insertion_sort
    print(f"AVG CASE execution time for INSERTION SORT: {avgcase_time_taken_insertion_sort}")

    bestcase_arr_insertion_sort = []
    for i in range(0, user_input):
        bestcase_arr_insertion_sort.append(i)
    # print(f"Original Array: {bestcase_arr_insertion_sort}")
    bestcase_start_time_insertion_sort = time.time()
    insertion_sort(bestcase_arr_insertion_sort)
    # print(f"Sorted Array: {bestcase_arr_insertion_sort}")
    bestcase_end_time_insertion_sort = time.time()
    bestcase_time_taken_insertion_sort = bestcase_end_time_insertion_sort - bestcase_start_time_insertion_sort
    print(f"BEST CASE execution time for INSERTION SORT: {bestcase_time_taken_insertion_sort}")

    worstcase_arr_insertion_sort = []
    for j in range(user_input, -1, -1):
        worstcase_arr_insertion_sort.append(j)
    # print(f"Original Array: {worstcase_arr_insertion_sort}")
    worstcase_start_time_insertion_sort = time.time()
    insertion_sort(worstcase_arr_insertion_sort)
    # print(f"Sorted Array: {worstcase_arr_insertion_sort}")
    worstcase_end_time_insertion_sort = time.time()
    worstcase_time_taken_insertion_sort = worstcase_end_time_insertion_sort - worstcase_start_time_insertion_sort
    print(f"WORST CASE execution time for INSERTION SORT: {worstcase_time_taken_insertion_sort}")

    plt.clf()
    labels= ["BEST", "AVG", "WORST"]
    plt.bar(labels, [bestcase_time_taken_insertion_sort, avgcase_time_taken_insertion_sort, worstcase_time_taken_insertion_sort])
    plt.title("Insertion Sort Execution Time")
    plt.xlabel("Types of cases")
    plt.ylabel("Execution time")
    plt.plotsize(50, 30)
    plt.show()