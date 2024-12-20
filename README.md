# Puzzle Solver

This project is a Python implementation of a general-purpose puzzle solver, designed to handle sliding puzzles of any size (e.g., 8-puzzle, 15-puzzle). It uses heuristic search algorithms like Best-First Search to efficiently find solutions. The solver includes multiple heuristic functions to evaluate and compare puzzle states.

## Features
- **Customizable Puzzle Size:** Define the size of the puzzle (e.g., 3x3, 4x4).
- **Goal State Generator:** Automatically generates the goal state for the given puzzle size.
- **Solvability Check:** Verifies if a given puzzle state is solvable.
- **Efficient Search Algorithm:** Uses Best-First Search with heuristics for optimal performance.
- **Multiple Heuristics:** Supports Manhattan Distance, Misplaced Tiles, Euclidean Distance, and Linear Conflict heuristics.

## Project Structure

- `PuzzleSolver` class:
  - Handles puzzle initialization, solvability checks, solving the puzzle, and generating neighbors.
- Heuristic functions:
  - `manhattan_distance`
  - `misplaced_tiles`
  - `euclidean_distance`
  - `linear_conflict`

## Usage

### Prerequisites
- Python 3.7 or higher

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```

### Example
```python
from solver import PuzzleSolver, manhattan_distance

# Define the puzzle size (e.g., 3x3)
puzzle_size = 3

# Initial puzzle state (example for 8-puzzle)
start_state = [1, 2, 3, 4, 5, 6, 0, 7, 8]

# Initialize the solver with Manhattan Distance heuristic
solver = PuzzleSolver(puzzle_size, manhattan_distance)

# Check if the puzzle is solvable
if solver.is_solvable(start_state):
    result = solver.solve(start_state)
    print(f"Solution: {result['solution']}")
    print(f"Steps: {result['steps']}")
    print(f"Time Taken: {result['time']} seconds")
else:
    print("The puzzle is not solvable.")
```

## Heuristics
1. **Manhattan Distance:**
   - Calculates the sum of distances of all tiles from their goal positions.
2. **Misplaced Tiles:**
   - Counts the number of tiles not in their goal positions.
3. **Euclidean Distance:**
   - Computes the straight-line distance between current and goal positions.
4. **Linear Conflict:**
   - Adds a penalty for tiles that are in the correct row/column but in conflict with others.

## Key Methods
- `generate_goal_state()`: Generates the goal state for the puzzle.
- `is_solvable(puzzle)`: Checks if a given puzzle state is solvable.
- `solve(start_state)`: Solves the puzzle using Best-First Search.
- `get_neighbors(zero_index, state)`: Generates all possible moves from the current state.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
