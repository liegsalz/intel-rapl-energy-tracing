import random
from linux_impl import monitor_power_usage
from typing import Dict

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2 
        l = arr[:mid]
        r = arr[mid:]

        merge_sort(l)
        merge_sort(r)

        i = j = k = 0

        while i < len(l) and j < len(r):
            if l[i] < r[j]:
                arr[k] = l[i]
                i += 1
            else:
                arr[k] = r[j]
                j += 1
            k += 1

        while i < len(l):
            arr[k] = l[i]
            i += 1
            k += 1

        while j < len(r):
            arr[k] = r[j]
            j += 1
            k += 1
    
    return arr

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break
    
    return arr

def generate_random_array(size=10000, min_value=0, max_value=100000):
    """
    Generates an array with `size` elements with random values between `min_value` and `max_value`.

    args:
    size: The number of elements in the array.
    min_value: The minimum value for the random numbers.
    max_value: The maximum value for the random numbers.

    Returns:
    The array with random values.
    """
    return [random.randint(min_value, max_value) for _ in range(size)]


def fibonacci_non_optimized(n):
    """
    A CPU-intensive function to calculate the n-th Fibonacci number using recursion.
    This naive approach has exponential time complexity O(2^n).
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_non_optimized(n - 1) + fibonacci_non_optimized(n - 2)

def fibonacci_memo(n: int, memo: Dict[int, int] = {}) -> int:
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]

def monitor_in_separate_process(pid: int):
    """
    This function will be run in a separate process.
    It calls the monitor_power_usage function with the given PID.
    """
    monitor_power_usage(pid)
    
def sum_of_squares_unoptimized(n):
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total

def sum_of_squares_optimized(n):
    return sum(i * i for i in range(1, n + 1))