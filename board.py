import pygame
import numpy as np
from sudoku_solver import SudokuSolver
from square import Square
import constants
from time import sleep

class Board:

    def __init__(self, win, matrix):
        self.win = win
        # Store initial matrix and solve it in text form
        self.start_matrix = np.copy(matrix)
        self.current_matrix = matrix
        self.solver = SudokuSolver(matrix)
        self.solution = self.solver.solve()

        self.squares = []
        self.selected_square = None

        self.draw_grid()
        
    def draw_grid(self):
        """
        Draws the 9x9 Sudoku grid.
        """
        for i in range(constants.ROWS):
            self.squares.append([])

            for j in range(constants.COLS):
                new_square = Square(self.win, i, j, self.start_matrix[i, j])
                new_square.draw()
                new_square.write_initial_value()

                self.squares[i].append(new_square)

    def get_clicked_square(self, position):
        """
        Returns the row and column position of a clicked square.

        Arguments:
            - position: Tuple containing the x and y coordinates of the point which is clicked.
        """

        # Find the column
        column = -1
        for square in self.squares[0]:
            if square.xcord > position[0]:
                break
            else:
                column += 1

        row = -1
        for j in range(constants.ROWS):
            if self.squares[j][column].ycord > position[1]:
                break
            else:
                row += 1

        return row, column


    def select_square(self, row, column):
        """
        Selects the square in given row and column.

        Arguments:
            - row: Row of square to select (int 0-8)
            - column: Column of square to select (int 0-8)
        """

        if self.selected_square is not None:
            # Remove border for prior selected square
            self.selected_square.deselect()

            # Redraw red/green borders for surrounding cells
            prior_row = self.selected_square.row 
            prior_col = self.selected_square.col

            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for horiz, vert in dirs:
                new_row = prior_row + vert
                new_col = prior_col + horiz

                if (0 <= new_row < 9) and (0 <= new_col < 9):
                    is_correct = self.squares[new_row][new_col].is_correct
                    if is_correct >= 0:
                        self.squares[new_row][new_col].draw_border(bool(is_correct))


        self.squares[row][column].select()
        self.selected_square = self.squares[row][column]

    def move_selected(self, direction):
        """
        Selects the square in a given direction from the currently selected square.

        Arguments:
            - direction: String representing direction to move. Can be one of 4 values: 'up', 'down', 'left', or 'right'.
        """
        if self.selected_square is not None:
            current_row = self.selected_square.row
            current_col = self.selected_square.col

            if direction.lower() == 'up':
                if current_row != 0:
                    self.select_square(current_row - 1, current_col)

            elif direction.lower() == 'down':
                if current_row != 8:
                    self.select_square(current_row + 1, current_col)

            elif direction.lower() == 'right':
                if current_col != 8:
                    self.select_square(current_row, current_col + 1)

            elif direction.lower() == 'left':
                if current_col != 0:
                    self.select_square(current_row, current_col - 1)

    def update_square(self, value):
        """
        Updates the selected square with a given value. If value is 0, the square is cleared.

        Arguments:
            - value: New value to update square.
        """
        if self.selected_square:
            self.selected_square.update_value(value)
            self.current_matrix[self.selected_square.row, self.selected_square.col] = value
            
            # Update green/red border
            if self.selected_square.is_correct >= 0:
                is_correct = (value == self.solution[self.selected_square.row, self.selected_square.col])
                self.selected_square.draw_border(is_correct)

    def check_square(self, row, column):
        """
        Checks if square in given row and column has the correct value in it, drawing green border if it is correct, and
        red if not. Removes border if the square is already being checked.
        """

        if self.squares[row][column].is_correct == -1:
            is_correct = self.squares[row][column].value == self.solution[row, column]
            self.squares[row][column].draw_border(is_correct)

        else:
            self.squares[row][column].remove_border()

    def solved(self):
        """
        Tells user the the Sudoku has been solved correctly.
        """
        pygame.font.init()
        font = pygame.font.SysFont('calibri', 150)

        text_surface = font.render("Solved!", 1, constants.PINK)
        self.win.blit(text_surface, (150, 300))

    def reset(self):
        """
        Resets the board to the original starting matrix, and removes all green and red borders.
        """
        for i in range(constants.ROWS):
            for j in range(constants.COLS):
                self.current_matrix[i, j] = self.start_matrix[i, j]
                self.squares[i][j].update_value(self.current_matrix[i, j])
                self.squares[i][j].remove_border()
    
    def solve_gui(self):
        """
        Solves the sudoku puzzle.
        """

        self.reset()
        start_i, start_j = self.next_loc(0, 0)
        self.find_solution(start_i, start_j)
    
    def find_solution(self, i, j):
        """
        Recursive method using backtracking algorithm to solve the Sudoku puzzle and redraw the GUI at each step.

        Arguments:
            - i: current row of square to solve.
            - j: current column of square to solve.
        """

        # Base case
        if 0 not in self.current_matrix:
            # Only need to check full validity if no empty cells are present (like in case that Solver is passed a bad full matrix)
            # Otherwise algorithm will ensure validity at all steps
            return True

        else:
            num = 1
            is_solution = False

            while num < 10 and not is_solution:
                # Check if num is valid in position (i,j)
                if self.is_valid_element(num, i, j):
                    self.current_matrix[i, j] = num
                    
                    self.select_square(i, j)
                    if self.selected_square.is_correct < 0:
                        self.check_square(i, j)

                    self.update_square(num)
                    pygame.display.update()

                    # Sleep so it isn't solved too quickly
                    sleep(0.02)
                
                    # Determine next position to fill
                    next_i, next_j = self.next_loc(i, j)

                    # Recursivly see if this leads to a solution.
                    is_solution = self.find_solution(next_i, next_j)
    
                num += 1

            # Reset to 0 (empty) if all numbers tried and no solution in this path
            if not is_solution:
                self.current_matrix[i, j] = 0
                self.select_square(i, j)
                self.update_square(0)
                pygame.display.update()

                
            return is_solution

    def is_valid_element(self, num, row, col):
        """
        Returns True if num is a valid entry in position (i, j). According to Sudoku rules, there can be no duplicates along a 
        given row or column, and there must be no duplicates in each 3x3 submatrix.
        Arguments:
            - num: int. Number 1-9 to check
            - row: int. Row number between 0 and 8
            - col: int. Column number between 0 and 8
        """

        # Check if duplicate in row 
        for j in range(constants.COLS):
            if j != col and self.current_matrix[row, j] == num:
                return False
        
        # Check if duplicate in col
        for i in range(constants.ROWS):
            if i != row and self.current_matrix[i, col] == num:
                return False

        # Check if duplicate in submatrix
        submatrix_loc = self.get_submatrix_coord(row, col)

        for i in range(submatrix_loc[0], submatrix_loc[0] + 3):
            for j in range(submatrix_loc[1], submatrix_loc[1] + 3):
                if (i, j) != (row, col) and self.current_matrix[i, j] == num:
                    return False
                
        return True

    def get_submatrix_coord(self, row, col):
        """
        Returns the coordinates of the top left element of the submatrix which contains row i and column j.
        """
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3

        return (row_start, col_start)

    def next_loc(self, i, j):
        """
        Returns a tuple for the next empty location to check. Traversal order is left to right, then top to bottom. 
        """
        next_i, next_j = i, j

        while next_i < 9 and next_j < 9 and self.current_matrix[next_i, next_j] != 0:
            next_i = next_i if next_j < 8 else next_i + 1
            next_j = next_j + 1 if next_j < 8 else 0

        return next_i, next_j

