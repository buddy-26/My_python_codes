graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [], 'E': [], 'F': []
}

def bfs(start_node):
    queue = [start_node] # Pehle node ko queue mein daalo
    visited = []         # Jo check ho gaye unki list

    while queue:
        # 1. Queue se sabse aage wala nikalo (FIFO)
        person = queue.pop(0) 
        
        if person not in visited:
            print(f"Visiting: {person}")
            visited.append(person)
            
            # 2. Uske saare doston ko line (Queue) mein piche khada kar do
            for friend in graph[person]:
                queue.append(friend)

bfs('A')
