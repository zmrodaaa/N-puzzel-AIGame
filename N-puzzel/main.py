import tkinter as tk
from tkinter import ttk, messagebox
from solver import PuzzleSolver, manhattan_distance, misplaced_tiles, euclidean_distance, linear_conflict
import random


class N_Puzzle_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent N-Puzzle Solver")
        
        self.size = 3
        self.state = []
        self.solver = None
        self.heuristics = {
            "Manhattan Distance": manhattan_distance,
            "Misplaced Tiles": misplaced_tiles,
            "Euclidean Distance": euclidean_distance,
            "Linear Conflict": linear_conflict
        }
        self.selected_heuristic = tk.StringVar(value="Manhattan Distance")
        
        self.root.geometry("550x650")
        self.root.config(bg="#e6f7ff")
        
        self.create_widgets()

    def create_widgets(self):
        heuristic_label = tk.Label(self.root, text="Choose Heuristic:", font=("Arial", 16), bg="#e6f7ff", fg="#003366")
        heuristic_label.pack(pady=10)
        
        heuristic_menu = ttk.Combobox(
            self.root, textvariable=self.selected_heuristic, values=list(self.heuristics.keys()), state="readonly",
            font=("Arial", 14)
        )
        heuristic_menu.pack(pady=10)
        
        random_button = tk.Button(self.root, text="Generate Random Puzzle", command=self.generate_random_puzzle,
                                  font=("Arial", 14), bg="#ffb3b3", relief="raised", width=20)
        random_button.pack(pady=15)
        
        self.puzzle_frame = tk.Frame(self.root, bg="#e6f7ff")
        self.puzzle_frame.pack(pady=20)
        
        solve_button = tk.Button(self.root, text="Solve Puzzle", command=self.solve_puzzle,
                                 font=("Arial", 14), bg="#80b3ff", relief="raised", width=20)
        solve_button.pack(pady=15)
        
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#e6f7ff", fg="#003366")
        self.result_label.pack(pady=20)

    def generate_random_puzzle(self):
        self.state = [i for i in range(self.size ** 2)]
        random.shuffle(self.state)
        
        while not PuzzleSolver(self.size, manhattan_distance).is_solvable(self.state):
            random.shuffle(self.state)
        
        self.display_puzzle(self.state)
    
    def display_puzzle(self, state):
        for widget in self.puzzle_frame.winfo_children():
            widget.destroy()
        
        for i, tile in enumerate(state):
            row, col = divmod(i, self.size)
            tile_text = str(tile) if tile != 0 else ""
            tile_color = "#c2f0ff" if tile == 0 else "#ffffb3"
            tile_label = tk.Label(self.puzzle_frame, text=tile_text, width=4, height=2, borderwidth=2, relief="groove", 
                                  font=("Arial", 18), bg=tile_color, fg="#003366")
            tile_label.grid(row=row, column=col, padx=5, pady=5)

    def solve_puzzle(self):
        if not self.state:
            messagebox.showerror("Error", "Please generate a puzzle first!")
            return
        
        heuristic_function = self.heuristics[self.selected_heuristic.get()]
        self.solver = PuzzleSolver(self.size, heuristic_function)
        
        result = None
        def solve():
            nonlocal result
            result = self.solver.solve(self.state)
            if result:
                solution_path = result["solution"]
                self.result_label.config(
                    text=f"Solved in {result['steps']} steps, Time: {result['time']} seconds"
                )
                self.animate_solution(solution_path)
            else:
                messagebox.showerror("Error", "No solution found!")
        
        self.root.after(100, solve)

    def animate_solution(self, solution_path):
        current_state = self.state[:]
        
        def update_puzzle(step):
            if step < len(solution_path):
                move = solution_path[step]
                zero_index = current_state.index(0)
                neighbors = self.solver.get_neighbors(zero_index, current_state)
                for direction, new_state in neighbors:
                    if direction == move:
                        current_state[:] = new_state
                        break
                self.display_puzzle(current_state)
                self.root.after(500, lambda: update_puzzle(step + 1))
        
        update_puzzle(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = N_Puzzle_GUI(root)
    root.mainloop()




