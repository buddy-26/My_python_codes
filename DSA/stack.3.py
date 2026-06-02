# TOPIC: Stack (LIFO - Last In First Out)
# Logic: Undo button ya folder structure mein piche jaane ke liye.

history = ["Home_Page", "Settings", "Privacy_Settings"]

# Piche jaane ke liye aakhiri item nikalo
if history:
    last_visited = history.pop() # Index nahi diya matlab aakhiri niklega
    print(f"Going back from: {last_visited}")
    print(f"Now you are at: {history[-1]}")
