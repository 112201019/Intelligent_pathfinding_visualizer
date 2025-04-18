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
    maze = generate_maze(80, 40)
    serialized = {f"{x},{y}": [f"{n[0]},{n[1]}" for n in neighbors] for (x, y), neighbors in maze.items()}
    return jsonify({'maze': serialized})

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    try:
        maze_data = data['maze']['maze']
        # print(data.keys())
        start = tuple(map(int, data['start'].split(',')))
        end = tuple(map(int, data['end'].split(',')))
        algorithm=data['algorithm']
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
        elif algorithm=="A*_cheby":
            visited, path, maxspace, visitedlength, lenpath= a_starC(maze, start, end)
        elif algorithm=="A*_wall":
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
    app.run(debug=True, host="10.32.5.70", port=5000)