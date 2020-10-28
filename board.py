import pygame
import numpy as np
from sudoku_solver import SudokuSolver
from square import Square
import constants
from time import sleep
from random import choice

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
                new_square.write_value()

                self.squares[i].append(new_square)

    def get_clicked_square(self, position):
        """
        Returns the row and column position of a clicked square.
        Arguments:
        position - tuple. The x and y coordinates of the point which is clicked.
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
        direction - str. Can be one of 4 values: 'up', 'down', 'left', or 'right'
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
        """
        if self.selected_square is not None:
            self.selected_square.update_value(value)
            self.current_matrix[self.selected_square.row, self.selected_square.col] = value
            
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
        self.reset()
        start_i, start_j = self.next_loc(0, 0)
        self.find_solution(start_i, start_j)
    
    def find_solution(self, i, j):

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
                    sleep(0.01)
                
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

def main():
    """
    Runs the game.
    """

    WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption('Sudoku')
    
    run = True
    freeze = False
    clock = pygame.time.Clock()
    matrix = get_start_matrix()
    board = Board(WIN, matrix)
    

    # Event loop
    while run:
        clock.tick(constants.FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not freeze:
                if event.type == pygame.KEYDOWN:
                    # Update values
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        board.update_square(1)

                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        board.update_square(2)

                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        board.update_square(3)

                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        board.update_square(4)

                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        board.update_square(5)

                    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        board.update_square(6)

                    elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        board.update_square(7)

                    elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        board.update_square(8)

                    elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        board.update_square(9)

                    elif event.key == pygame.K_DELETE:
                        board.update_square(0)

                    # Move selected
                    elif event.key == pygame.K_UP:
                        board.move_selected('up')
                    
                    elif event.key == pygame.K_DOWN:
                        board.move_selected('down')
                    
                    elif event.key == pygame.K_RIGHT:
                        board.move_selected('right')

                    elif event.key == pygame.K_LEFT:
                        board.move_selected('left')

                    # Reset board
                    elif event.key == pygame.K_r:
                        board.reset()

                    # Solve sudoku
                    elif event.key == pygame.K_SPACE:
                        board.solve_gui()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Left click
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        row, column = board.get_clicked_square(pos)
                        board.select_square(row, column)

                    # Right click
                    elif event.button == 3:
                        pos = pygame.mouse.get_pos()
                        row, column = board.get_clicked_square(pos)
                        board.check_square(row, column)

        pygame.display.update()

        if np.array_equal(board.solution, board.current_matrix):
            board.solved()
            freeze = True


    pygame.quit()


def get_start_matrix():
    """
    Returns the starting Sudoku matrix where 0 represents empty square.
    """

    mat_list = []
    mat_list.append(np.array([[0, 0, 0, 0, 0, 3, 0, 2, 7],
                            [1, 0, 0, 0, 0, 4, 6, 0, 3],
                            [0, 0, 0, 6, 0, 0, 0, 1, 0],
                            [6, 8, 5, 0, 7, 0, 1, 3, 2],
                            [7, 0, 0, 1, 6, 0, 5, 0, 8],
                            [0, 1, 9, 5, 0, 0, 0, 0, 4],
                            [9, 0, 0, 0, 4, 0, 0, 7, 1],
                            [0, 0, 0, 7, 2, 6, 0, 0, 0],
                            [0, 7, 3, 8, 9, 1, 0, 5, 0]]))

    mat_list.append(np.array([[0, 8, 4, 9, 0, 0, 7, 5, 0],
                                [3, 0, 6, 4, 0, 5, 2, 0, 8],
                                [0, 5, 0, 0, 0, 2, 4, 0, 6],
                                [0, 1, 5, 0, 0, 8, 9, 0, 2],
                                [9, 0, 8, 6, 0, 0, 0, 0, 4],
                                [7, 6, 3, 0, 4, 9, 1, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 1],
                                [0, 0, 0, 5, 2, 7, 6, 4, 9],
                                [0, 0, 0, 1, 0, 0, 0, 0, 0]]))

    # Medium
    mat_list.append(np.array([[0, 0, 0, 8, 0, 0, 6, 9, 0],
                                [0, 2, 6, 3, 0, 9, 0, 8, 5],
                                [0, 0, 1, 0, 0, 0, 0, 0, 7],
                                [0, 7, 0, 0, 0, 2, 5, 6, 0],
                                [0, 0, 0, 0, 9, 8, 0, 0, 0],
                                [0, 3, 8, 0, 6, 0, 9, 2, 0],
                                [0, 0, 0, 0, 2, 7, 0, 5, 0],
                                [6, 0, 0, 0, 0, 0, 0, 3, 0],
                                [0, 0, 4, 6, 0, 0, 7, 0, 0]]))

    mat_list.append(np.array([[0, 1, 3, 0, 0, 0, 8, 2, 0],
                                [0, 5, 0, 0, 0, 1, 0, 0, 0],
                                [0, 0, 0, 0, 7, 0, 5, 0, 0],
                                [0, 0, 0, 0, 5, 7, 0, 9, 6],
                                [0, 4, 0, 3, 0, 0, 0, 0, 8],
                                [0, 0, 0, 2, 8, 0, 7, 0, 3],
                                [0, 2, 9, 0, 6, 3, 0, 0, 0],
                                [3, 0, 8, 0, 0, 0, 0, 0, 0],
                                [0, 6, 1, 9, 2, 0, 0, 0, 4]]))


    return choice(mat_list)
    


main()
