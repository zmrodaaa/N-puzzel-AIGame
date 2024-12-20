

import heapq
import time

class PuzzleSolver:
    def __init__(self, size, heuristic_function):
        self.size = size
        self.heuristic_function = heuristic_function
        self.goal_state = self.generate_goal_state()
    
    def generate_goal_state(self):
        """Generate the goal state for the puzzle."""
        return [i for i in range(1, self.size ** 2)] + [0]
    
    def is_solvable(self, puzzle):
        """Check if the puzzle is solvable."""
        inversions = 0
        flat_puzzle = [tile for tile in puzzle if tile != 0]
        for i in range(len(flat_puzzle)):
            for j in range(i + 1, len(flat_puzzle)):
                if flat_puzzle[i] > flat_puzzle[j]:
                    inversions += 1
        if self.size % 2 == 1:
            return inversions % 2 == 0
        else:
            blank_row = self.size - (puzzle.index(0) // self.size)
            return (inversions + blank_row) % 2 == 0
    
    def solve(self, start_state):
        """Solve the puzzle using Best-First Search."""
        start_time = time.time()
        open_list = []
        closed_set = set()
        heapq.heappush(open_list, (0, start_state, []))
        
        while open_list:
            cost, current_state, path = heapq.heappop(open_list)
            if current_state == self.goal_state:
                end_time = time.time()
                return {
                    "solution": path,
                    "steps": len(path),
                    "time": round(end_time - start_time, 3)
                }
            closed_set.add(tuple(current_state))
            
            zero_index = current_state.index(0)
            neighbors = self.get_neighbors(zero_index, current_state)
            
            for move, new_state in neighbors:
                if tuple(new_state) not in closed_set:
                    new_cost = cost + self.heuristic_function(new_state, self.goal_state)
                    heapq.heappush(open_list, (new_cost, new_state, path + [move]))
        return None
    
    def get_neighbors(self, zero_index, state):
        """Generate all possible moves."""
        neighbors = []
        row, col = divmod(zero_index, self.size)
        moves = {
            "up": (row - 1, col),
            "down": (row + 1, col),
            "left": (row, col - 1),
            "right": (row , col + 1)  # corrected neighbor move
        }
        for move, (r, c) in moves.items():
            if 0 <= r < self.size and 0 <= c < self.size:
                new_state = state[:]
                new_index = r * self.size + c
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                neighbors.append((move, new_state))
        return neighbors


# /*///////////////////////////////////////////////////////////////////////////////////////*/

def manhattan_distance(state, goal_state):
    """Calculate Manhattan Distance heuristic."""
    size = int(len(state) ** 0.5)
    distance = 0
    for i, tile in enumerate(state):
        if tile != 0:
            goal_index = goal_state.index(tile)
            current_row, current_col = divmod(i, size)
            goal_row, goal_col = divmod(goal_index, size)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def misplaced_tiles(state, goal_state):
    """Count the number of misplaced tiles."""
    return sum(1 for i in range(len(state)) if state[i] != 0 and state[i] != goal_state[i])

def euclidean_distance(state, goal_state):
    """Calculate Euclidean Distance heuristic."""
    size = int(len(state) ** 0.5)
    distance = 0
    for i, tile in enumerate(state):
        if tile != 0:
            goal_index = goal_state.index(tile)
            current_row, current_col = divmod(i, size)
            goal_row, goal_col = divmod(goal_index, size)
            distance += ((current_row - goal_row) ** 2 + (current_col - goal_col) ** 2) ** 0.5
    return distance

def linear_conflict(state, goal_state):
    """Calculate Linear Conflict heuristic."""
    conflict = 0
    size = int(len(state) ** 0.5)
    
    for row in range(size):
        row_tiles = [state[row * size + col] for col in range(size)]
        goal_row_tiles = [goal_state[row * size + col] for col in range(size)]
        
        for i in range(size):
            for j in range(i + 1, size):
                if (row_tiles[i] != 0 and row_tiles[j] != 0 and 
                    (row_tiles[i] in goal_row_tiles and row_tiles[j] in goal_row_tiles) and 
                    goal_row_tiles.index(row_tiles[i]) > goal_row_tiles.index(row_tiles[j])):
                    conflict += 2
                    
    return manhattan_distance(state, goal_state) + conflict