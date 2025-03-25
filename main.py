from maze import *
from visualization import *
from traversal import *
from colours import *

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