'''def countdown(n):
    if n == 0:
        print("Blast Off! 🚀")
    else:
        print(n)
        countdown(n - 1) # <--- Ye hai wo girgit!

countdown(5)'''

class WarehouseSystem:
    def __init__(self):
        # 1. Stack: Inspection के लिए (LIFO)
        self.inspection_stack = []
        # 2. Queue: Delivery के लिए (FIFO)
        self.delivery_queue = []
        # 3. Graph: रास्तों का नक्शा
        self.road_map = {
            "Warehouse": "Sector_A",
            "Sector_A": "Customer_Home"
        }

    def process_new_item(self, item_id, item_name):
        print(f"\n--- Processing: {item_name} (ID: {item_id}) ---")

        # स्टेप 1: BST Logic (Decision Making)
        if item_id > 500:
            print(f"Decision: {item_name} is a High-Priority item.")
            
            # स्टेप 2: Stack (Adding to Inspection)
            self.inspection_stack.append(item_name)
            print(f"Added to Stack: {self.inspection_stack}")

            # स्टेप 3: Stack to Queue (Transferring)
            # यहाँ सामान Stack से निकलेगा (pop) और Queue में जाएगा (append)
            item_to_move = self.inspection_stack.pop()
            self.delivery_queue.append(item_to_move)
            print(f"Moved to Delivery Queue: {self.delivery_queue}")

            # स्टेप 4: Graph (Pathfinding)
            route = self.road_map["Warehouse"]
            print(f"Route Found: Warehouse -> {route}")
        else:
            print("Decision: Low priority, keeping in storage.")

    def ship_item(self):
        # स्टेप 5: Queue Logic (FIFO - First In First Out)
        if self.delivery_queue:
            shipped_item = self.delivery_queue.pop(0) # इंडेक्स 0 ही Queue की पहचान है!
            print(f"\n🚀 SHIPPED: {shipped_item} is on its way to the customer!")
        else:
            print("\nQueue is empty, nothing to ship.")

# --- सिस्टम को चला कर देखते हैं ---
wh = WarehouseSystem()

# 1. पहला सामान (Mobile - High ID)
wh.process_new_item(700, "Mobile")

# 2. दूसरा सामान (Laptop - High ID)
wh.process_new_item(800, "Laptop")

# 3. शिपिंग (FIFO के हिसाब से पहले Mobile जाएगा, फिर Laptop)
wh.ship_item()
wh.ship_item()
