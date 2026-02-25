# DFS with stack (LIFO)

# using a tree to find the dfs of this tree
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': []
}

def dfs_with_stack(tree, start_node, goal_node): # function for the dfs with stack along with its 3 parameters tree, start_node, and goal_node.
    visited = set()
    dfs_stack = [start_node] # creating stack
    
    while dfs_stack:
        next_node = dfs_stack.pop() # Pop last element (LIFO behavior of stack)
        
        if next_node not in visited: # Process node only if not already visited
            print(next_node, end=" ")
            visited.add(next_node)
            
            if next_node == goal_node: # if goal node is reached
                print("Goal Reached!")
                return visited
            
            for child in reversed(tree[next_node]): # Adding child in reverse position so that it will follow the path correctly.
                if child not in visited:
                    dfs_stack.append(child)
    
    return visited

visited = dfs_with_stack(tree, 'A', 'G') # Execute DFS starting from 'A' and searching for goal 'G'