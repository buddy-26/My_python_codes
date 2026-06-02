# TOPIC: Linked List (Chain of Nodes)
# Logic: Har item (Node) ke paas apna data aur agle item ka address hota hai.

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

# Use:
llist = LinkedList()
llist.append("File_A")
llist.append("File_B")
