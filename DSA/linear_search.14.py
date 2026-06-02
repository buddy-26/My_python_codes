# TOPIC: Linear Search (Ek-ek karke check karna)
# Logic: Poori list mein shuru se aakhiri tak dhoondo.

def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return f"Found at index {i}"
    return "Not found"

data = [4, 2, 7, 1, 9]
print(linear_search(data, 7))
