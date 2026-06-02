# TOPIC: Merge Sort (Divide and Conquer)
# Logic: List ko tab tak aadha karo jab tak 1 element na bache, phir sort karke jodo.

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    return result + left + right

data = [99, 12, 45, 1, 67, 34]
print(f"Merge Sorted: {merge_sort(data)}")
