# TOPIC: Binary Search (Divide and Conquer)
# Logic: Har baar list ko aadha (half) karke search karna.

def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return f"Found at index {mid}"
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return "Not Found"

# Sorted list honi chahiye
sorted_files = [101, 205, 308, 410, 502, 607]
print(binary_search(sorted_files, 410))
