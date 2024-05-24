import tkinter as tk
from tkinter import messagebox
import random


class SudokuGUI:
    def __init__(self, master):
        # initialize Sudoku GUI
        self.master = master
        self.master.title("Sudoku Solver") # title of the window
        self.master.geometry("350x400") # size of the window

        # colors for the grid
        self.colors = ["#B8D0EB", "#AB8CD7"]

        # Create buttons for Sudoku
        self.generate_button = tk.Button(self.master, text="Generate Sudoku", command=self.generate_sudoku,
                                         bg="#4CAF50", fg="white")
        self.generate_button.grid(row=0, column=0, padx=5, pady=5)

        self.solve_button = tk.Button(self.master, text="Solve Sudoku", command=self.solve_sudoku, bg="#008CBA",
                                      fg="white")
        self.solve_button.grid(row=0, column=1, padx=5, pady=5)

        self.user_solve_button = tk.Button(self.master, text="Check User Solve", command=self.user_solve_sudoku, bg="#FFA500",
                                           fg="white")
        self.user_solve_button.grid(row=0, column=2, padx=5, pady=5)

        # Create a frame
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Create an empty Sudoku grid
        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                # Determine the background color of the cell based on its position
                ##########
                color_index = (i // 3) * 3 + j // 3
                color = self.colors[color_index % len(self.colors)]
                # Create an Entry widget for each cell
                cell = tk.Entry(self.grid_frame, width=2, font=('Arial', 20), bg=color)
                cell.grid(row=i, column=j, padx=1, pady=1)
                # Add validation to ensure only single-digit numbers are entered
                cell.config(validate="key", validatecommand=(cell.register(self.on_validate), '%P'))
                row.append(cell)
            self.cells.append(row)

    def on_validate(self, value):
        # Validation function to allow only single-digit numbers
        if value.isdigit():
            # Ensure only single-digit numbers are allowed
            return len(value) == 1
        elif value == "":
            # Allow empty string
            return True
        else:
            # Disallow non-digit characters
            return False

    def print_grid(self, grid):
        # Fill in the Sudoku grid based on the provided puzzle
        for i in range(9):
            for j in range(9):
                # If the cell value is not zero, insert the value into the cell
                if grid[i][j] != 0:
                    self.cells[i][j].insert(0, str(grid[i][j]))
                # If the cell value is zero, delete any existing value in the cell
                else:
                    self.cells[i][j].delete(0, tk.END)

    def clear_grid(self):
        # Clear the entire Sudoku grid by deleting all values in each cell
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)

    def is_valid_move(self, grid, row, col, num):
        # Check if the number is already in the row
        if num in grid[row]:
            return False

        # Check if the number is already in the column9
        if num in [grid[i][col] for i in range(9)]:
            return False

        # Check if the number is already in the 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == num:
                    return False

        return True



    def find_empty_cell(self, grid):
        # Find the first empty cell (cell with value 0) in the Sudoku grid
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return i, j  # Return the row and column of the empty cell
        return None  # Return None if no empty cell is found

    def solve_sudoku(self):
        # Solve the Sudoku puzzle
        grid = self.get_grid()  # Get the current state of the Sudoku grid
        if self.solve(grid):  # If a solution is found
            self.print_grid(grid)  # Print the solved Sudoku grid
        else:
            messagebox.showinfo("Sudoku Solver", "No solution exists!")  # Show a message if no solution exists

    def solve(self, grid):
        # Recursively solve the Sudoku puzzle using backtracking
        empty_cell = self.find_empty_cell(grid)  # Find an empty cell in the grid
        if not empty_cell:  # If no empty cell is found, the puzzle is solved
            return True

        row, col = empty_cell  # Get the row and column of the empty cell

        for num in range(1, 10):  # Try numbers from 1 to 9
            if self.is_valid_move(grid, row, col, num):  # If the number is a valid move
                grid[row][col] = num  # Place the number in the empty cell
                if self.solve(grid):  # Recursively solve the rest of the puzzle
                    return True
                grid[row][col] = 0  # If no solution is found, backtrack by resetting the cell to 0
        return False  # Return False if no valid number can be placed in the empty cell

    def generate_sudoku(self):
        # Generate a new Sudoku puzzle
        grid = [[0] * 9 for _ in range(9)]  # Create an empty Sudoku grid
        self.solve(grid)  # Start with a solved puzzle
        # Remove random cells to create the puzzle
        for _ in range(45):  # Adjust difficulty by changing the number of removed cells
            row, col = random.randint(0, 8), random.randint(0, 8)
            while grid[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            grid[row][col] = 0
        self.clear_grid()  # Clear the grid before printing the new puzzle
        self.print_grid(grid)  # Print the new Sudoku puzzle

    def get_grid(self):
        # Get the current state of the Sudoku grid
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.cells[i][j].get()  # Get the value of the cell
                if value.isdigit():
                    row.append(int(value))  # Convert the value to an integer and add it to the row
                else:
                    row.append(0)  # If the value is not a digit, add 0 to the row
            grid.append(row)  # Add the row to the grid
        return grid  # Return the Sudoku grid

    def user_solve_sudoku(self):
        # Allow the user to solve the Sudoku puzzle
        grid = self.get_grid()  # Get the current state of the Sudoku grid
        if self.solve(grid):  # If the puzzle is solved
            if all(all(cell.get() != '' for cell in row) for row in self.cells):
                messagebox.showinfo("Sudoku Solver", "Congratulations! You solved the puzzle.")
            else:
                messagebox.showinfo("Sudoku Solver", "There are still empty cells.")
        else:
            messagebox.showinfo("Sudoku Solver", "No solution exists!")


def main():
    # Main function to create and run the Sudoku GUI
    root = tk.Tk()  # Create the main window
    app = SudokuGUI(root)  # Create an instance of the SudokuGUI class
    root.mainloop()  # Run the main event loop


if __name__ == "__main__":
    main()
