WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 50, 255)
NAVY_BLUE = (190, 230, 255)
YELLOW = (255, 223, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
STATS_FONT_COLOR = (0, 0, 0)
STATS_FONT_SIZE = 24

import random
from collections import deque
from colours import *
import pygame
import time
import math
import heapq
import pygame

def initAdjacencyList(width, height):
    adjacency_list = {}
    for x in range(width):
        for y in range(height):
            adjacency_list[(x, y)] = []
    return adjacency_list

def neighbours(x, y, width, height):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []
    for dx, dy in directions:
        X, Y = x + dx, y + dy
        if 0 <= X < width and 0 <= Y < height:
            neighbors.append((X, Y))
    return neighbors

def generate_maze(width, height, start=(0, 0)):
    maze = initAdjacencyList(width, height)
    stack = [start]
    visited = set([start])

    while stack:
        x, y = stack[-1]
        neighbors = [n for n in neighbours(x, y, width, height) if n not in visited]
        if neighbors:
            next_cell = random.choice(neighbors)
            maze[(x, y)].append(next_cell)
            maze[next_cell].append((x, y))
            stack.append(next_cell)
            visited.add(next_cell)
        else:
            stack.pop()
    
    for ele in maze.keys():
        if random.randint(0, 100000000) % 3 == 0:
            feasible = [(1,0), (-1,0), (0,1), (0,-1)]
            listt = []
            for dx, dy in feasible:
                if 0 <= ele[0] + dx < width and 0 <= ele[1] + dy < height:
                    listt.append((ele[0] + dx, ele[1] + dy))
            if listt:
                randd = random.choice(listt)
                if randd not in maze[ele]:
                    maze[ele].append(randd)
                    maze[randd].append(ele)
    return maze

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



WIDTH, HEIGHT = 30, 30
CELL_SIZE = 30
SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE + 50

DIJKSTRA_BUTTON_POS = ((WIDTH * CELL_SIZE)/2 - 50, SCREEN_HEIGHT - 45)
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 40
DFS_BUTTON_POS = (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 45)
BFS_BUTTON_POS = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 45)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze traversal visualizer")
screen.fill(WHITE)

def draw_maze(maze):
    for (x, y), neighbors in maze.items():
        cx, cy = x * CELL_SIZE, y * CELL_SIZE
        if (x, y - 1) not in neighbors:
            pygame.draw.line(screen, BLACK, (cx, cy), (cx + CELL_SIZE, cy), 3)
        else:
            pygame.draw.line(screen, GRAY, (cx, cy), (cx + CELL_SIZE, cy), 2)
        if (x + 1, y) not in neighbors:
            pygame.draw.line(screen, BLACK, (cx + CELL_SIZE, cy), (cx + CELL_SIZE, cy + CELL_SIZE), 3)
        else:
            pygame.draw.line(screen, GRAY, (cx + CELL_SIZE, cy), (cx + CELL_SIZE, cy + CELL_SIZE), 2)
        if (x, y + 1) not in neighbors:
            pygame.draw.line(screen, BLACK, (cx, cy + CELL_SIZE), (cx + CELL_SIZE, cy + CELL_SIZE), 3)
        else:
            pygame.draw.line(screen, GRAY, (cx, cy + CELL_SIZE), (cx + CELL_SIZE, cy + CELL_SIZE), 2)
        if (x - 1, y) not in neighbors:
            pygame.draw.line(screen, BLACK, (cx, cy), (cx, cy + CELL_SIZE), 3)
        else:
            pygame.draw.line(screen, GRAY, (cx, cy), (cx, cy + CELL_SIZE), 2)

def draw_button(text, pos, color):
    font = pygame.font.Font(None, 30)
    rect = pygame.Rect(pos[0], pos[1], BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, WHITE)
    screen.blit(label, (pos[0] + 20, pos[1] + 10))
    return rect

def reset_maze(maze):
    screen.fill(WHITE)
    draw_maze(maze)
    dfs_button = draw_button("DFS", DFS_BUTTON_POS, BLACK)
    bfs_button = draw_button("BFS", BFS_BUTTON_POS, BLACK)
    A_star_button1 = draw_button("A*.M", (BFS_BUTTON_POS[0]+150, BFS_BUTTON_POS[1]), BLACK)
    A_star_button2 = draw_button("A*.E", (BFS_BUTTON_POS[0]+300, BFS_BUTTON_POS[1]), BLACK)
    pygame.display.flip()

def draw_cell(x, y, color):
    margin = 3
    pygame.draw.rect(screen, color, (x * CELL_SIZE + margin, y * CELL_SIZE + margin, CELL_SIZE - 1 * margin, CELL_SIZE - 1 * margin))
    pygame.display.update()

def draw_arrow(start, end, color):
    x1, y1 = start[0] * CELL_SIZE + CELL_SIZE // 2, start[1] * CELL_SIZE + CELL_SIZE // 2
    x2, y2 = end[0] * CELL_SIZE + CELL_SIZE // 2, end[1] * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), 3)
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_length = 8
    arrow_angle = math.pi / 6
    x3 = x2 - arrow_length * math.cos(angle - arrow_angle)
    y3 = y2 - arrow_length * math.sin(angle - arrow_angle)
    x4 = x2 - arrow_length * math.cos(angle + arrow_angle)
    y4 = y2 - arrow_length * math.sin(angle + arrow_angle)
    pygame.draw.polygon(screen, color, [(x2, y2), (x3, y3), (x4, y4)])
    

def show_stats1(screen, visited, time_taken, mode, length, lenn):
    font = pygame.font.Font(None, STATS_FONT_SIZE)
    
    stats_text = [
        f"Visited blocks: {visited}   Path length: {length}"
    ]
    
    y_position = SCREEN_HEIGHT - 35  # Above buttons
    for text in stats_text:
        label = font.render(text, True, STATS_FONT_COLOR)
        screen.blit(label, (20, y_position))
        y_position += 30
    
    pygame.display.flip()
    
def show_stats2(screen, visited, time_taken, mode, length, lenn):
    font = pygame.font.Font(None, STATS_FONT_SIZE)
    
    stats_text = [
        f"Time taken: {time_taken:.1f} secs     Mode: {mode}    Max space used: {lenn}"
    ]
    
    y_position = SCREEN_HEIGHT - 35  # Above buttons
    for text in stats_text:
        label = font.render(text, True, STATS_FONT_COLOR)
        screen.blit(label, (1300, y_position))
        y_position += 30
    
    pygame.display.flip()

def main():
    maze = generate_maze(WIDTH, HEIGHT)
    draw_maze(maze)
    dfs_button = draw_button("DFS", DFS_BUTTON_POS, BLACK)
    bfs_button = draw_button("BFS", BFS_BUTTON_POS, BLACK)
    A_star_button1 = draw_button("A*.M", (BFS_BUTTON_POS[0]+150, BFS_BUTTON_POS[1]), BLACK)
    A_star_button2 = draw_button("A*.E", (BFS_BUTTON_POS[0]+300, BFS_BUTTON_POS[1]), BLACK)
    pygame.display.flip()
    
    selected_start = None
    selected_end = None
    selecting_start = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if dfs_button.collidepoint(x, y) or bfs_button.collidepoint(x, y) or A_star_button1.collidepoint(x, y) or A_star_button2.collidepoint(x, y):
                    start = selected_start if selected_start else (0, 0)
                    end = selected_end if selected_end else (WIDTH - 1, HEIGHT - 1)
                    if dfs_button.collidepoint(x, y):
                        dfs_traverse(maze, start, end)
                    elif bfs_button.collidepoint(x, y):
                        bfs_traverse(maze, start, end)
                    elif A_star_button1.collidepoint(x, y):
                        a_star_traverse1(maze, start, end)
                    elif A_star_button2.collidepoint(x, y):
                        a_star_traverse2(maze, start, end)
                        
                else:
                    grid_x = x // CELL_SIZE
                    grid_y = y // CELL_SIZE
                    if 0 <= grid_x < WIDTH and 0 <= grid_y < HEIGHT and y < (HEIGHT * CELL_SIZE):
                        if selecting_start:
                            selected_start = (grid_x, grid_y)
                            selecting_start = False
                        else:
                            selected_end = (grid_x, grid_y)
                            selecting_start = True
                        reset_maze(maze)
                        if selected_start:
                            draw_cell(selected_start[0], selected_start[1], GREEN)
                        if selected_end:
                            draw_cell(selected_end[0], selected_end[1], RED)
                        pygame.display.flip()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()