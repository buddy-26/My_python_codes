# TOPIC: Quick Sort (Pivot Logic)
# Logic: Ek 'Pivot' chun lo, usse chote left mein aur bade right mein daalo.

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

data = [10, 80, 30, 90, 40, 50, 70]
print(f"Quick Sorted: {quick_sort(data)}")
