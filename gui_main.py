import pygame
import constants
import numpy as np
from board import Board
from random import choice

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

                    # Update square values
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

                    # Move selected square
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

    return choice(mat_list)
    

if __name__ == '__main__':
    main()