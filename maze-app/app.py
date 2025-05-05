from flask import Flask, render_template, jsonify, request
from traversal import *
from maze import *
app = Flask(__name__)

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-maze')
def generate_maze_route():
    try:
        # --- FIX: Read width and height from query parameters ---
        default_width, default_height = 80, 40
        min_dim, max_dim = 10, 250 # Server-side limits

        width = request.args.get('width', default=default_width, type=int)
        height = request.args.get('height', default=default_height, type=int)

        # Clamp values to server limits
        width = max(min_dim, min(max_dim, width))
        height = max(min_dim, min(max_dim, height))
        # print(f"Generating maze with size: {width}x{height}") # Server log

        # --- FIX: Pass the received width and height to the generator ---
        maze = generate_maze(width, height)

        # Serialize keys as strings "x,y" for JSON compatibility
        serialized = {f"{x},{y}": [f"{n[0]},{n[1]}" for n in neighbors]
                      for (x, y), neighbors in maze.items()}

        return jsonify({'maze': serialized})
    except Exception as e:
        print(f"Error in /generate-maze: {e}")
        return jsonify({'error': f'Server error during maze generation: {str(e)}'}), 500
@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    try:
        maze_data = data['maze']['maze']
        # print(data.keys())
        start = tuple(map(int, data['start'].split(',')))
        end = tuple(map(int, data['end'].split(',')))
        algorithm=data['algorithm']
        print(algorithm)
        maze = {}
        for cell_str, neighbors_str in maze_data.items():
            x, y = map(int, cell_str.split(','))
            maze[(x, y)] = [tuple(map(int, n.split(','))) for n in neighbors_str]
        if algorithm=="BFS":
            visited, path, maxspace, visitedlength, lenpath = bfs(maze, start, end)
        elif algorithm=="DFS":    
            visited, path, maxspace, visitedlength, lenpath= dfs(maze, start, end)
        elif algorithm=="A*_Manhattan":
            visited, path, maxspace, visitedlength, lenpath= a_starM(maze, start, end)
        elif algorithm=="A*_Euclidean":
            visited, path, maxspace, visitedlength, lenpath= a_starE(maze, start, end)
        elif algorithm=="A*_chebyshev":
            visited, path, maxspace, visitedlength, lenpath= a_starC(maze, start, end)
        elif algorithm=="A*_ManhattanWallHeuristic":
            visited, path, maxspace, visitedlength, lenpath= a_star_enhanced(maze, start, end, 1)
            
        
        return jsonify({
            'visited': [f"{x},{y}" for x, y in visited],
            'path': [f"{x},{y}" for x, y in path],
            'maxspace': maxspace,
            'visitedlength':visitedlength,
            'lenpath': lenpath
        })
        
    except KeyError as e:
        return jsonify({'error': f'Missing key in request data: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)