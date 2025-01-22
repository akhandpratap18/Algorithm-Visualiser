import streamlit as st
import random
import matplotlib.pyplot as plt
import time

# Sorting Algorithms
def bubble_sort(arr):
    steps = []
    n = len(arr)
    step_number = 1
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                reason = f"Swapped because {arr[j]} is greater than {arr[j + 1]}."
            else:
                reason = f"No swap because {arr[j]} is less than or equal to {arr[j + 1]}."
            steps.append((arr[:], j, j + 1, n - i - 1, step_number, reason))
            step_number += 1
    return steps

def insertion_sort(arr):
    steps = []
    step_number = 1
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            reason = f"Moved {arr[j]} because it is greater than {key}."
            steps.append((arr[:], i, j, len(arr), step_number, reason))
            step_number += 1
            j -= 1
        arr[j + 1] = key
        reason = f"Inserted {key} at position {j + 1}."
        steps.append((arr[:], i, j + 1, len(arr), step_number, reason))
        step_number += 1
    return steps

def selection_sort(arr):
    steps = []
    step_number = 1
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
            reason = f"Selected {arr[min_idx]} as the smallest value."
            steps.append((arr[:], i, min_idx, len(arr), step_number, reason))
            step_number += 1
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        reason = f"Swapped {arr[i]} with {arr[min_idx]}."
        steps.append((arr[:], i, min_idx, len(arr), step_number, reason))
        step_number += 1
    return steps

def merge_sort(arr):
    steps = []
    step_number = 1

    def merge_sort_helper(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_helper(arr, left, mid)
            merge_sort_helper(arr, mid + 1, right)
            merge(arr, left, mid, right)

    def merge(arr, left, mid, right):
        nonlocal step_number
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                reason = f"Inserted {left_part[i]} from left part because it is smaller."
                i += 1
            else:
                arr[k] = right_part[j]
                reason = f"Inserted {right_part[j]} from right part because it is smaller."
                j += 1
            steps.append((arr[:], left, right, len(arr), step_number, reason))
            step_number += 1
            k += 1
        while i < len(left_part):
            arr[k] = left_part[i]
            reason = f"Inserted {left_part[i]} from left part because no elements remain in the right part."
            steps.append((arr[:], left, right, len(arr), step_number, reason))
            step_number += 1
            i += 1
            k += 1
        while j < len(right_part):
            arr[k] = right_part[j]
            reason = f"Inserted {right_part[j]} from right part because no elements remain in the left part."
            steps.append((arr[:], left, right, len(arr), step_number, reason))
            step_number += 1
            j += 1
            k += 1

    merge_sort_helper(arr, 0, len(arr) - 1)
    return steps

# Searching Algorithms
def linear_search(arr, target):
    steps = []
    for idx, value in enumerate(arr):
        if value == target:
            reason = f"Found {target} at index {idx}."
        else:
            reason = f"{value} is not equal to {target}."
        steps.append((arr[:], idx, target, reason))
        if value == target:
            break
    return steps

def binary_search(arr, target):
    steps = []
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            reason = f"Found {target} at index {mid}."
            steps.append((arr[:], mid, target, reason))
            break
        elif arr[mid] < target:
            reason = f"{arr[mid]} is less than {target}, searching the right half."
            left = mid + 1
        else:
            reason = f"{arr[mid]} is greater than {target}, searching the left half."
            right = mid - 1
        steps.append((arr[:], mid, target, reason))
    return steps

def visualize_steps(steps, algorithm):
    placeholder = st.empty()
    for step in steps:
        if algorithm in ["Linear Search", "Binary Search"]:
            arr, idx, target, reason = step
            # Highlight the found element in blue
            colors = [
                'blue' if i == idx and arr[i] == target else 'red' if i == idx else 'skyblue'
                for i in range(len(arr))
            ]
        else:
            arr, idx1, idx2, _, _, reason = step
            colors = ['red' if i in [idx1, idx2] else 'skyblue' for i in range(len(arr))]

        with placeholder.container():
            fig, ax = plt.subplots()
            bars = ax.bar(range(len(arr)), arr, color=colors)
            # Annotate values on top of bars
            for bar, value in zip(bars, arr):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                        str(value), ha='center', va='bottom', fontsize=8)

            ax.set_xlabel("Index")
            ax.set_ylabel("Value")
            ax.set_title(f"{algorithm} Visualization")
            st.pyplot(fig)
            plt.close(fig)

        st.write(f"**Explanation:** {reason}")
        time.sleep(0.5)



# Streamlit UI
st.title("Algorithm Visualizer")

# Select Mode
mode = st.selectbox("Choose Mode", ["Sorting", "Searching"])

# State to hold the array
if "array" not in st.session_state:
    st.session_state["array"] = []

if mode == "Sorting":
    # Algorithm Selector
    algorithm = st.selectbox(
        "Choose a Sorting Algorithm",
        ["Bubble Sort", "Insertion Sort", "Selection Sort", "Merge Sort"]
    )

    # Array Size
    array_size = st.slider("Array Size", min_value=5, max_value=50, value=10)

    # Animation Speed
    speed = st.slider("Animation Speed (ms)", min_value=50, max_value=1000, value=300)

    # Regenerate Array Button
    if st.button("Regenerate Array") or not st.session_state["array"]:
        st.session_state["array"] = random.sample(range(1, 101), array_size)

    arr = st.session_state["array"]
    st.write("Initial Array:", arr)

    # Visualize Button
    if st.button("Visualize Sorting"):
        steps = []
        if algorithm == "Bubble Sort":
            steps = bubble_sort(arr)
        elif algorithm == "Insertion Sort":
            steps = insertion_sort(arr)
        elif algorithm == "Selection Sort":
            steps = selection_sort(arr)
        elif algorithm == "Merge Sort":
            steps = merge_sort(arr)

        visualize_steps(steps, algorithm)

elif mode == "Searching":
    # Algorithm Selector
    algorithm = st.selectbox(
        "Choose a Searching Algorithm",
        ["Linear Search", "Binary Search"]
    )

    # Array Size
    array_size = st.slider("Array Size", min_value=5, max_value=50, value=10)

    # Regenerate Array Button
    if st.button("Regenerate Array") or not st.session_state["array"]:
        st.session_state["array"] = sorted(random.sample(range(1, 101), array_size))

    arr = st.session_state["array"]
    st.write("Sorted Array:", arr)

    # Target Value
    target = st.number_input("Enter Target Value", min_value=1, max_value=100)

    # Visualize Button
    if st.button("Visualize Searching"):
        steps = []
        if algorithm == "Linear Search":
            steps = linear_search(arr, target)
        elif algorithm == "Binary Search":
            steps = binary_search(arr, target)

        visualize_steps(steps, algorithm)
