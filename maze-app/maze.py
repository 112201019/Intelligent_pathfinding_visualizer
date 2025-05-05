import random
# Helper functions
def init_adjacency_list(width, height):
    return {(x, y): [] for x in range(width) for y in range(height)}

def neighbours(x, y, width, height):
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    return [(x+dx, y+dy) for dx, dy in dirs if 0 <= x+dx < width and 0 <= y+dy < height]

# Maze generation
def generate_maze(width, height):
    maze = init_adjacency_list(width, height)
    stack = [(0, 0)]
    visited = set(stack)

    while stack:
        x, y = stack[-1]
        candidates = [n for n in neighbours(x, y, width, height) if n not in visited]
        
        if candidates:
            next_cell = random.choice(candidates)
            maze[(x, y)].append(next_cell)
            maze[next_cell].append((x, y))
            stack.append(next_cell)
            visited.add(next_cell)
        else:
            stack.pop()

    # Add random connections
    for cell in maze:
        if random.randint(0, 3) == 0:  # 25% chance
            x, y = cell
            possible = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
            valid = [(a,b) for a,b in possible if 0<=a<width and 0<=b<height]
            if valid:
                neighbor = random.choice(valid)
                if neighbor not in maze[cell]:
                    maze[cell].append(neighbor)
                    maze[neighbor].append(cell)
    # print(maze)
    return maze