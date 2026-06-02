# TOPIC: Binary Search Tree (Left Chota, Right Bada)
# Logic: Har node ke left mein chota aur right mein bada data hota hai.

class BSTNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return BSTNode(key)
    else:
        if root.val < key:
            root.right = insert(root.right, key)
        else:
            root.left = insert(root.left, key)
    return root

# Root node banayein
root = BSTNode(50)
root = insert(root, 30)
root = insert(root, 70)
