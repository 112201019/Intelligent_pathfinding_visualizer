from collections import deque
import heapq
import random

def dfs(maze, start, end):
    visited_order = []
    stack = [start]
    visited = set()
    path = {}

    while stack:
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
    
    return visited_order, final_path

def bfs(maze, start, end):
    visited_order = []
    stack = [start]
    visited = set()
    path = {}

    while stack:
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
    
    return visited_order, final_path

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_starM(maze, start, end):
    visited_order = []
    visited = set()
    path = {}
    priority_queue = []
    g_cost = {start: 0}
    heapq.heappush(priority_queue, (manhattan_distance(start, end), start))
    
    while priority_queue:
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
    
    return visited_order, final_path

def EuclideanDistance(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2

def a_starE(maze, start, end):
    visited_order = []
    visited = set()
    path = {}
    priority_queue = []
    g_cost = {start: 0}
    heapq.heappush(priority_queue, (EuclideanDistance(start, end), start))
    
    while priority_queue:
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
    
    return visited_order, final_path
