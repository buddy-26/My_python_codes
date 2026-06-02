# TOPIC: BFS (Breadth-First Search)
# Logic: Pehle saare padosi (neighbors) ko check karo.

def bfs_logic(start_node, graph):
    queue = [start_node]
    visited = []
    
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
            print(f"Connected to: {node}")
            queue.extend(graph[node]) # Saare padosi line mein lagao

# Graph example
network = {'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}
bfs_logic('A', network)
