# TOPIC: DFS (Depth-First Search)
# Logic: Ek raaste par tab tak jao jab tak khatam na ho jaye, phir piche aao.

def dfs_logic(node, graph, visited=None):
    if visited is None:
        visited = set()
    
    if node not in visited:
        print(f"Deep Scanning: {node}")
        visited.add(node)
        for neighbor in graph[node]:
            dfs_logic(neighbor, graph, visited)

# Example Graph
folder_tree = {'Root': ['Folder1', 'Folder2'], 'Folder1': ['FileA'], 'Folder2': [], 'FileA': []}
dfs_logic('Root', folder_tree)
