def merge_sort(arr):
    # Base Case: Agar list mein 1 hi item hai, toh wo sorted hai
    if len(arr) <= 1:
        return arr

    # 1. DIVIDE: Beech ka point dhundho
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # 2. RECURSION: Dono hisson ko phir se sort karne bhejo
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)

    # 3. MERGE: Ab dono ko sahi order mein jodo
    return merge(left_sorted, right_sorted)

def merge(left, right):
    sorted_list = []
    # Yahan hum dono lists ke aage wale items ko compare karte hain
    # Jo chota hota hai, use pehle 'append' karte hain
    while left and right:
        if left[0] < right[0]:
            sorted_list.append(left.pop(0))
        else:
            sorted_list.append(right.pop(0))
    
    # Jo bacha kucha hai use jodo
    return sorted_list + left + right

# Chala kar dekhte hain
my_list = [38, 27, 43, 3, 9, 82, 10]
print("Final Sorted List:", merge_sort(my_list))
