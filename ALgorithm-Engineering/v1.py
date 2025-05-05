import heapq
import math
import pygame
import sys # To cleanly exit

# --- Dijkstra and Graph Building (from previous code) ---

def build_graph(intersections, roads):
    """Converts intersection and road lists into an adjacency list graph."""
    graph = {intersection: [] for intersection in intersections}
    for u, v, weight in roads:
        # Assuming roads are two-way
        if u in graph and v in graph:
            graph[u].append((v, weight))
            graph[v].append((u, weight))
        else:
            print(f"Warning: Road ({u}, {v}) involves unknown intersection(s). Skipping.")
    return graph

def dijkstra(graph, start_node, end_node):
    """
    Finds the shortest path between start_node and end_node in a weighted graph
    using Dijkstra's algorithm.

    Returns:
        tuple: (path, total_distance)
               path (list): The sequence of nodes in the shortest path.
               total_distance (float): The total weight of the shortest path.
               Returns ([], float('inf')) if no path exists.
    """
    if start_node not in graph or end_node not in graph:
        return [], float('inf')

    distances = {node: float('inf') for node in graph}
    previous_nodes = {node: None for node in graph}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]
    path_found = False # Flag to check if end_node was reached

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        # Check if we've reached the destination *after* popping it
        # This ensures we process the final node correctly
        if current_node == end_node:
             path_found = True
             # We could break here for efficiency if only one path needed
             # break

        for neighbor, weight in graph.get(current_node, []):
            distance_through_current = distances[current_node] + weight
            if distance_through_current < distances[neighbor]:
                distances[neighbor] = distance_through_current
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance_through_current, neighbor))

    # Reconstruct path only if the end node was reachable
    path = []
    if path_found and distances[end_node] != float('inf'):
        current = end_node
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        path.reverse()
        return path, distances[end_node]
    else:
         # Return empty path and infinity if end_node wasn't reached or distance is inf
        return [], float('inf')


# --- Pygame Visualization Settings ---
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("City Map Pathfinding Visualization")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (50, 100, 200)
GREEN = (50, 200, 100)
RED = (200, 50, 50)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240) # Highlight color for path

# Font
NODE_FONT_SIZE = 20
WEIGHT_FONT_SIZE = 16
INFO_FONT_SIZE = 22
node_font = pygame.font.SysFont(None, NODE_FONT_SIZE)
weight_font = pygame.font.SysFont(None, WEIGHT_FONT_SIZE)
info_font = pygame.font.SysFont(None, INFO_FONT_SIZE)


# Node properties
NODE_RADIUS = 15

# --- Map Data and Coordinates ---
intersections = ["A", "B", "C", "D", "E", "F", "G", "H"]
roads = [
    ("A", "B", 5), ("A", "C", 8), ("B", "D", 3), ("B", "E", 6),
    ("C", "D", 2), ("C", "F", 4), ("D", "E", 1), ("D", "G", 9),
    ("E", "G", 3), ("F", "G", 2), ("F", "H", 7), ("G", "H", 4),
]

# Assign screen coordinates to intersections (adjust these as needed)
node_positions = {
    "A": (100, 150), "B": (250, 100), "C": (150, 300), "D": (300, 250),
    "E": (450, 150), "F": (300, 450), "G": (500, 350), "H": (650, 450)
}

# --- Drawing Functions ---

def draw_map(graph, node_positions, path_nodes=None, path_edges=None, start_node=None, end_node=None):
    """Draws the graph on the Pygame screen."""
    screen.fill(WHITE) # Clear screen with background color

    if path_nodes is None: path_nodes = set()
    if path_edges is None: path_edges = set()

    # 1. Draw Edges (draw lines first so nodes are on top)
    drawn_edges = set() # To avoid drawing bidirectional edges twice
    for u, neighbors in graph.items():
        pos_u = node_positions.get(u)
        if not pos_u: continue

        for v, weight in neighbors:
            pos_v = node_positions.get(v)
            if not pos_v: continue

            # Ensure edge isn't drawn twice (A->B and B->A)
            edge = tuple(sorted((u, v)))
            if edge in drawn_edges:
                continue
            drawn_edges.add(edge)

            # Determine color and thickness
            is_path_edge = edge in path_edges
            edge_color = PURPLE if is_path_edge else GRAY
            edge_thickness = 3 if is_path_edge else 1

            pygame.draw.line(screen, edge_color, pos_u, pos_v, edge_thickness)

            # Draw edge weight (optional)
            mid_x = (pos_u[0] + pos_v[0]) // 2
            mid_y = (pos_u[1] + pos_v[1]) // 2
            weight_text = weight_font.render(str(weight), True, BLACK)
            screen.blit(weight_text, (mid_x + 5, mid_y - 15)) # Offset slightly

    # 2. Draw Nodes
    for node, pos in node_positions.items():
        # Determine color based on role
        node_color = BLUE # Default
        if node == start_node:
            node_color = GREEN
        elif node == end_node:
            node_color = RED
        elif node in path_nodes:
            node_color = PURPLE # Intermediate path node

        pygame.draw.circle(screen, node_color, pos, NODE_RADIUS)
        pygame.draw.circle(screen, BLACK, pos, NODE_RADIUS, 1) # Black border

        # Draw node label
        text_surf = node_font.render(node, True, BLACK)
        text_rect = text_surf.get_rect(center=pos)
        screen.blit(text_surf, text_rect)

def draw_info(start_node, end_node, total_distance):
    """Displays information about the path found."""
    if total_distance == float('inf'):
        info_text = f"No path found from {start_node} to {end_node}"
        color = RED
    elif total_distance == 0 and start_node == end_node:
         info_text = f"Start and End are the same: {start_node}"
         color = BLACK
    else:
        info_text = f"Shortest Path: {start_node} to {end_node} | Distance: {total_distance:.2f}"
        color = BLACK

    text_surf = info_font.render(info_text, True, color)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, 30)) # Position at top-center
    screen.blit(text_surf, text_rect)

# --- Main Program Logic ---

if __name__ == "__main__":
    # 1. Build the graph
    city_graph = build_graph(intersections, roads)

    # 2. Get User Input (outside Pygame loop for simplicity here)
    start_node_input = ""
    end_node_input = ""
    while start_node_input not in city_graph:
        start_node_input = input(f"Enter start intersection {list(city_graph.keys())}: ").strip().upper()
        if start_node_input not in city_graph:
            print("Invalid start intersection.")

    while end_node_input not in city_graph:
        end_node_input = input(f"Enter end intersection {list(city_graph.keys())}: ").strip().upper()
        if end_node_input not in city_graph:
            print("Invalid end intersection.")


    # 3. Find Shortest Path using Dijkstra
    shortest_path_nodes, path_distance = dijkstra(city_graph, start_node_input, end_node_input)

    # Prepare path data for drawing
    path_nodes_set = set(shortest_path_nodes)
    path_edges_set = set()
    if shortest_path_nodes:
        for i in range(len(shortest_path_nodes) - 1):
            u, v = shortest_path_nodes[i], shortest_path_nodes[i+1]
            # Store edge uniquely, regardless of direction
            path_edges_set.add(tuple(sorted((u, v))))

    print("-" * 30)
    if shortest_path_nodes:
        print(f"Shortest path found: {' -> '.join(shortest_path_nodes)}")
        print(f"Total distance: {path_distance}")
    else:
        print(f"No path found from {start_node_input} to {end_node_input}.")
    print("-" * 30)
    print("Starting Pygame visualization...")

    # 4. Pygame Main Loop
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Allow exiting with ESC key
                    running = False

        # Drawing
        draw_map(city_graph, node_positions, path_nodes_set, path_edges_set, start_node_input, end_node_input)
        draw_info(start_node_input, end_node_input, path_distance)

        # Update display
        pygame.display.flip()

        # Cap frame rate
        clock.tick(30) # Limit to 30 FPS

    pygame.quit()
    sys.exit()