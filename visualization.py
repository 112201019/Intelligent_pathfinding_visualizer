import pygame
import time
import math
from colours import *


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