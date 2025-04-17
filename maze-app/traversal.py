from collections import deque
import heapq
import random

def dfs(maze, start, end):
    visited_order = []
    stack = [start]
    visited = set()
    path = {}
    maxsize=0

    while stack:
        maxsize=max(maxsize, len(stack))
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)
        
        if current == end:
            break
            
        for neighbor in maze[current]:
            if neighbor not in visited:
                stack.append(neighbor)
                path[neighbor] = current
        

    # Reconstruct path
    final_path = []
    node = end
    while node in path:
        final_path.append(node)
        node = path[node]
    final_path.reverse()
    print(len(visited), len(final_path), maxsize)
    return visited_order, final_path, maxsize, len(visited), len(final_path)

def bfs(maze, start, end):
    visited_order = []
    stack = [start]
    visited = set()
    path = {}
    maxsize=0

    while stack:
        maxsize=max(maxsize, len(stack))
        current = stack.pop(0)
        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)
        
        if current == end:
            break
            
        for neighbor in maze[current]:
            if neighbor not in visited:
                stack.append(neighbor)
                path[neighbor] = current

    # Reconstruct path
    final_path = []
    node = end
    while node in path:
        final_path.append(node)
        node = path[node]
    final_path.reverse()
    print(len(visited), len(final_path))
    
    return visited_order, final_path, maxsize, len(visited), len(final_path)

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_starM(maze, start, end):
    visited_order = []
    visited = set()
    path = {}
    maxsize=0
    priority_queue = []
    g_cost = {start: 0}
    heapq.heappush(priority_queue, (manhattan_distance(start, end), start))
    
    while priority_queue:
        maxsize = max(maxsize, len(priority_queue))
        f_cost, current = heapq.heappop(priority_queue)
        
        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)
        
        if current == end:
            break
        
        for neighbor in maze[current]:
            new_g = g_cost[current] + 1  # Assuming uniform cost for each step
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                new_f = new_g + manhattan_distance(neighbor, end)
                heapq.heappush(priority_queue, (new_f, neighbor))
                path[neighbor] = current

    # Reconstruct path from end to start
    final_path = []
    node = end
    while node in path:
        final_path.append(node)
        node = path[node]
    final_path.reverse()
    
    return visited_order, final_path, maxsize, len(visited), len(final_path)

def EuclideanDistance(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2) **0.5

def a_starE(maze, start, end):
    visited_order = []
    visited = set()
    path = {}
    priority_queue = []
    maxsize=0
    g_cost = {start: 0}
    heapq.heappush(priority_queue, (EuclideanDistance(start, end), start))
    
    while priority_queue:
        maxsize = max(maxsize, len(priority_queue))
        f_cost, current = heapq.heappop(priority_queue)
        
        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)
        
        if current == end:
            break
        
        for neighbor in maze[current]:
            new_g = g_cost[current] + 1  # Assuming uniform cost for each step
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                new_f = new_g + EuclideanDistance(neighbor, end)
                heapq.heappush(priority_queue, (new_f, neighbor))
                path[neighbor] = current

    # Reconstruct path from end to start
    final_path = []
    node = end
    while node in path:
        final_path.append(node)
        node = path[node]
    final_path.reverse()
    
    return visited_order, final_path, maxsize, len(visited), len(final_path)

def chebyshev_distance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def a_starC(maze, start, end):
    visited_order = []
    visited = set()
    path = {}
    priority_queue = []
    maxsize=0
    g_cost = {start: 0}
    heapq.heappush(priority_queue, (chebyshev_distance(start, end), start))
    
    while priority_queue:
        maxsize = max(maxsize, len(priority_queue))
        f_cost, current = heapq.heappop(priority_queue)
        
        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)
        
        if current == end:
            break
        
        for neighbor in maze[current]:
            new_g = g_cost[current] + 1  # Assuming uniform cost for each step
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                new_f = new_g + chebyshev_distance(neighbor, end)
                heapq.heappush(priority_queue, (new_f, neighbor))
                path[neighbor] = current

    # Reconstruct path from end to start
    final_path = []
    node = end
    while node in path:
        final_path.append(node)
        node = path[node]
    final_path.reverse()
    
    return visited_order, final_path, maxsize, len(visited), len(final_path)

import heapq
import random

def manhattan_distance(a, b):
    """Standard Manhattan distance between two points a and b.
       Points are represented as tuples (x, y)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def count_walls_on_path_maze(a, b, maze):
    """
    Given two grid points a and b, counts the number of walls encountered
    along two Manhattan traversal strategies (horizontal-then-vertical and vertical-then-horizontal)
    by checking connectivity in the maze (i.e. if a connection does not exist in the adjacency list, 
    then we treat that as a wall).
    
    Returns the minimum wall count.
    """
    x1, y1 = a
    x2, y2 = b

    def walls_horiz_then_vert():
        walls = 0
        path = []
        # Horizontal movement: from (x1, y1) to (x2, y1)
        step_x = 1 if x2 >= x1 else -1
        for x in range(x1, x2, step_x):
            curr = (x, y1)
            nxt = (x + step_x, y1)
            path.append((curr, nxt))
        # Vertical movement: from (x2, y1) to (x2, y2)
        step_y = 1 if y2 >= y1 else -1
        for y in range(y1, y2, step_y):
            curr = (x2, y)
            nxt = (x2, y + step_y)
            path.append((curr, nxt))
        
        for (cell, adjacent) in path:
            # If the connection is missing in the maze, count it as a wall.
            if adjacent not in maze[cell]:
                walls += 1
        return walls

    def walls_vert_then_horiz():
        walls = 0
        path = []
        # Vertical movement: from (x1, y1) to (x1, y2)
        step_y = 1 if y2 >= y1 else -1
        for y in range(y1, y2, step_y):
            curr = (x1, y)
            nxt = (x1, y + step_y)
            path.append((curr, nxt))
        # Horizontal movement: from (x1, y2) to (x2, y2)
        step_x = 1 if x2 >= x1 else -1
        for x in range(x1, x2, step_x):
            curr = (x, y2)
            nxt = (x + step_x, y2)
            path.append((curr, nxt))
            
        for (cell, adjacent) in path:
            if adjacent not in maze[cell]:
                walls += 1
        return walls

    # Return the minimum wall count of the two candidate traversals.
    return min(walls_horiz_then_vert(), walls_vert_then_horiz())

def enhanced_heuristic(a, b, maze, wall_weight=1):
    """
    Enhanced heuristic for A* in a maze represented as an adjacency list.
    
    It is defined as the Manhattan distance plus a penalty equal to
    wall_weight times the minimum number of missing connections (walls)
    along a straight-line (Manhattan) traversal between a and b.
    """
    return manhattan_distance(a, b) + wall_weight * count_walls_on_path_maze(a, b, maze)

def a_star_enhanced(maze, start, end, wall_weight=1):
    """
    A* algorithm using an enhanced heuristic that accounts for both the Manhattan distance
    and the number of walls (missing connections) along the corridor.
    
    Parameters:
      - maze: Dictionary where keys are cells (tuples) and values are lists of neighbors.
      - start, end: Tuples representing the start and end coordinates.
      - wall_weight: Factor to weight the wall penalty.
    
    Returns:
      - visited_order: List of cells in the order they were visited.
      - final_path: List of cells from start to end (if a path exists).
    """
    visited_order = []
    visited = set()
    came_from = {}
    g_cost = {start: 0}
    maxsize=0

    # Priority queue items are tuples: (f_cost, cell)
    priority_queue = []
    initial_f = enhanced_heuristic(start, end, maze, wall_weight)
    heapq.heappush(priority_queue, (initial_f, start))
    
    while priority_queue:
        maxsize = max(maxsize, len(priority_queue))
        f_cost, current = heapq.heappop(priority_queue)
        
        if current in visited:
            continue
        
        visited.add(current)
        visited_order.append(current)
        
        if current == end:
            break
        
        for neighbor in maze[current]:
            tentative_g = g_cost[current] + 1  # Uniform cost for each step
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                f = tentative_g + enhanced_heuristic(neighbor, end, maze, wall_weight)
                heapq.heappush(priority_queue, (f, neighbor))
                came_from[neighbor] = current
    
    # Reconstruct the final path from end to start
    final_path = []
    node = end
    while node in came_from:
        final_path.append(node)
        node = came_from[node]
    final_path.reverse()
    
    return visited_order, final_path, maxsize, len(visited), len(final_path)


