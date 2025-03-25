import random
from collections import deque
from colours import *


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