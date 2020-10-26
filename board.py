import pygame
import numpy as np
from sudoku_solver import SudokuSolver
from square import Square
import constants

class Board:

    def __init__(self, win, matrix):
        self.win = win
        # Store initial matrix and solve it in text form
        self.start_matrix = matrix
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
        if self.selected_square is not None:
            self.selected_square.deselect()

        self.squares[row][column].select()
        self.selected_square = self.squares[row][column]

    def move_selected(self, direction):
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
        if self.selected_square is not None:
            self.selected_square.update_value(value)
            self.current_matrix[self.selected_square.row, self.selected_square.col] = value
            
            if self.selected_square.is_correct >= 0:
                is_correct = (value == self.solution[self.selected_square.row, self.selected_square.col])
                self.selected_square.draw_border(is_correct)

    def check_square(self, row, column):
        if self.squares[row][column].is_correct == -1:
            is_correct = self.squares[row][column].value == self.solution[row, column]
            self.squares[row][column].draw_border(is_correct)

        else:
            self.squares[row][column].remove_border()

    def solved(self):
        pygame.font.init()
        font = pygame.font.SysFont('calibri', 150)

        text_surface = font.render("Solved!", 1, constants.PINK)
        self.win.blit(text_surface, (150, 300))

    def solve_gui(self):
        pass

def main():
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

    return np.array([[0, 0, 0, 0, 0, 3, 0, 2, 7],
                    [1, 0, 0, 0, 0, 4, 6, 0, 3],
                    [0, 0, 0, 6, 0, 0, 0, 1, 0],
                    [6, 8, 5, 0, 7, 0, 1, 3, 2],
                    [7, 0, 0, 1, 6, 0, 5, 0, 8],
                    [0, 1, 9, 5, 0, 0, 0, 0, 4],
                    [9, 0, 0, 0, 4, 0, 0, 7, 1],
                    [0, 0, 0, 7, 2, 6, 0, 0, 0],
                    [0, 7, 3, 8, 9, 1, 0, 5, 0]])


main()
