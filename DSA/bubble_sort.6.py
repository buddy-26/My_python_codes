# TOPIC: Bubble Sort (Comparing Neighbors)
# Logic: Bagal wale se compare karo aur bada hai toh jagah badal do.

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                # Swapping (Jagah badalna)
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

prices = [500, 120, 350, 50, 200]
print(f"Sorted Prices: {bubble_sort(prices)}")
