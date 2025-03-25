import heapq
import pygame
import time
import math
from visualization import *
from collections import deque
from colours import *

    
def dfs_traverse(maze, start, end):
    start_time=time.time()
    reset_maze(maze)
    draw_cell(start[0], start[1], GREEN)
    draw_cell(end[0], end[1], RED)
    pygame.display.flip()
    stack = [start]
    visited = set()
    path = {start: None}
    maxx=0
    while stack:
        maxx=max(maxx, len(stack))
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        draw_cell(x, y, YELLOW)
        draw_cell(start[0], start[1], GREEN)
        draw_cell(end[0], end[1], RED)
        
        pygame.time.delay(1)
        
        if (x, y) == end:
            break
        
        for neighbor in maze[(x, y)]:
            if neighbor not in visited:
                stack.append(neighbor)
                path[neighbor] = (x, y)
    
    cell = end
    counter=0
    while cell in path:
        draw_cell(cell[0], cell[1], NAVY_BLUE)
        draw_cell(start[0], start[1], GREEN)
        draw_cell(end[0], end[1], RED)
        prev = path[cell]
        counter+=1
        if prev is not None:
            draw_arrow(prev, cell, BLACK)
        pygame.display.update()
        pygame.time.delay(1)
        cell = prev
    
    draw_cell(start[0], start[1], GREEN)
    draw_cell(end[0], end[1], RED)
    pygame.display.flip()
    
    # Calculate stats
    end_time = time.time()
    show_stats1(screen, len(visited), end_time - start_time, "DFS", counter, maxx)
    show_stats2(screen, len(visited), end_time - start_time, "DFS", counter, maxx)
    
    draw_cell(start[0], start[1], GREEN)
    draw_cell(end[0], end[1], RED)
    pygame.display.flip()

    
    

def bfs_traverse(maze, start, end):
    start_time=time.time()
    reset_maze(maze)
    draw_cell(start[0], start[1], GREEN)
    draw_cell(end[0], end[1], RED)
    pygame.display.flip()
    queue = [start]
    visited = set()
    path = {start: None}
    maxx=0
    while queue:
        maxx=max(maxx, len(queue))
        x, y = queue.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        draw_cell(x, y, YELLOW)
        draw_cell(start[0], start[1], GREEN)
        draw_cell(end[0], end[1], RED)
        pygame.time.delay(1)
        
        if (x, y) == end:
            break
        
        for neighbor in maze[(x, y)]:
            if neighbor not in visited:
                queue.append(neighbor)
                path[neighbor] = (x, y)
    
    cell = end
    counter=0
    while cell in path:
        draw_cell(cell[0], cell[1], NAVY_BLUE)
        draw_cell(start[0], start[1], GREEN)
        draw_cell(end[0], end[1], RED)
        counter+=1
        prev = path[cell]
        if prev is not None:
            draw_arrow(prev, cell, BLACK)
        pygame.display.update()
        pygame.time.delay(1)
        cell = prev
    
    draw_cell(start[0], start[1], GREEN)
    draw_cell(end[0], end[1], RED)
    pygame.display.flip()

    end_time = time.time()
    show_stats1(screen, len(visited), end_time - start_time, "BFS", counter, maxx)
    show_stats2(screen, len(visited), end_time - start_time, "BFS", counter, maxx)
    
    draw_cell(start[0], start[1], GREEN)
    draw_cell(end[0], end[1], RED)
    pygame.display.flip()


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_traverse1(maze, start, end):
    start_time = time.time()
    reset_maze(maze)
    draw_cell(start[0], start[1], GREEN)
    draw_cell(end[0], end[1], RED)
    pygame.display.flip()
    
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (priority, node)
    
    g_cost = {start: 0}  # Cost from start to current node
    path = {start: None}
    visited = set()
    maxx = 0
    
    while priority_queue:
        maxx = max(maxx, len(priority_queue))
        _, current = heapq.heappop(priority_queue)
        
        if current in visited:
            continue
        visited.add(current)
        
        draw_cell(current[0], current[1], YELLOW)
        draw_cell(start[0], start[1], GREEN)
        draw_cell(end[0], end[1], RED)
        pygame.time.delay(1)
        
        if current == end:
            break
        
        for neighbor in maze[current]:
            new_g = g_cost[current] + 1  # Uniform cost for all edges
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                f_cost = new_g + manhattan_distance(neighbor, end)
                heapq.heappush(priority_queue, (f_cost, neighbor))
                path[neighbor] = current
    
    # Reconstruct path
    cell = end
    counter = 0
    while cell in path:
        draw_cell(cell[0], cell[1], NAVY_BLUE)
        draw_cell(start[0], start[1], GREEN)
        draw_cell(end[0], end[1], RED)
        counter += 1
        prev = path[cell]
        if prev is not None:
            draw_arrow(prev, cell, BLACK)
        pygame.display.update()
        pygame.time.delay(1)
        cell = prev
    
    draw_cell(start[0], start[1], GREEN)
    draw_cell(end[0], end[1], RED)
    pygame.display.flip()
    
    end_time = time.time()
    show_stats1(screen, len(visited), end_time - start_time, "A*", counter, maxx)
    show_stats2(screen, len(visited), end_time - start_time, "A*", counter, maxx)
    
    draw_cell(start[0], start[1], GREEN)
    draw_cell(end[0], end[1], RED)
    pygame.display.flip()


def euclidean_distance(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5


def a_star_traverse2(maze, start, end):
    start_time = time.time()
    reset_maze(maze)
    draw_cell(start[0], start[1], GREEN)
    draw_cell(end[0], end[1], RED)
    pygame.display.flip()
    
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (priority, node)
    
    g_cost = {start: 0}  # Cost from start to current node
    path = {start: None}
    visited = set()
    maxx = 0
    
    while priority_queue:
        maxx = max(maxx, len(priority_queue))
        _, current = heapq.heappop(priority_queue)
        
        if current in visited:
            continue
        visited.add(current)
        
        draw_cell(current[0], current[1], YELLOW)
        draw_cell(start[0], start[1], GREEN)
        draw_cell(end[0], end[1], RED)
        pygame.time.delay(1)
        
        if current == end:
            break
        
        for neighbor in maze[current]:
            new_g = g_cost[current] + 1  # Uniform cost for all edges
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                f_cost = new_g + euclidean_distance(neighbor, end)
                heapq.heappush(priority_queue, (f_cost, neighbor))
                path[neighbor] = current
    
    # Reconstruct path
    cell = end
    counter = 0
    while cell in path:
        draw_cell(cell[0], cell[1], NAVY_BLUE)
        draw_cell(start[0], start[1], GREEN)
        draw_cell(end[0], end[1], RED)
        counter += 1
        prev = path[cell]
        if prev is not None:
            draw_arrow(prev, cell, BLACK)
        pygame.display.update()
        pygame.time.delay(1)
        cell = prev
    
    draw_cell(start[0], start[1], GREEN)
    draw_cell(end[0], end[1], RED)
    pygame.display.flip()
    
    end_time = time.time()
    show_stats1(screen, len(visited), end_time - start_time, "A*", counter, maxx)
    show_stats2(screen, len(visited), end_time - start_time, "A*", counter, maxx)
    
    draw_cell(start[0], start[1], GREEN)
    draw_cell(end[0], end[1], RED)
    pygame.display.flip()
