import constants
import pygame
from constants import SQUARE_SIZE

class Square:

    INNER_SQUARE_SIZE = SQUARE_SIZE - 2

    def __init__(self, win, i, j, value):
        self.win = win
        self.value = value
        self.row = i
        self.col = j
        self.set_pixel_location()

        self.selected = False
        self.can_write = (value == 0) # False if square contains a nonempty given starting value
        self.is_correct = -1 # -1 if not currently checked, 1 if correct value, 0 if not

    def set_pixel_location(self):
        """
        Sets the x coordinate and y coordinate pixel location of the square on the board.
        """

        r_triplet = 0 if self.row < 3 else 2 * (self.row // 3)
        c_triplet = 0 if self.col < 3 else 2 * (self.col // 3)

        self.xcord = self.col * SQUARE_SIZE + c_triplet
        self.ycord = self.row * SQUARE_SIZE + r_triplet

    def draw(self):
        """
        Draws square with black outline.
        """
        pygame.draw.rect(self.win, constants.BLACK, (self.xcord, self.ycord, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(self.win, constants.WHITE, (self.xcord + 1, self.ycord + 1, self.INNER_SQUARE_SIZE, self.INNER_SQUARE_SIZE))
    
    def write_initial_value(self):
        """
        Draws the given initial value in the square. Used to draw the starting numbers which cannot be changed.
        """
        
        if self.value > 0:
            pygame.font.init()
            font = pygame.font.SysFont('verdana', 70)

            text_surface = font.render(str(self.value), 1, constants.BLACK)

            i = self.xcord + int(0.3 * SQUARE_SIZE)
            j = self.ycord 
            
            self.win.blit(text_surface, (i, j))

    def update_value(self, value):
        """
        Updates the value of the square and redraws the new number.

        Arguments:
            - value: New value of the square between 0 and 9. 0 will clear the square.
        """

        if self.can_write:
            if value == 0:
                self.value = value
                self.delete_value()

            elif value > 0:
                self.value = value
                self.delete_value()

                pygame.font.init()
                font = pygame.font.SysFont('calibri', 75)

                text_surface = font.render(str(self.value), 1, constants.BLACK)

                i = self.xcord + int(0.3 * SQUARE_SIZE)
                j = self.ycord + int(0.15 * SQUARE_SIZE)
                
                self.win.blit(text_surface, (i, j))
            
    def delete_value(self):
        """
        Clears the displayed value in the square.
        """
        pygame.draw.rect(self.win, constants.WHITE, (self.xcord + 1, self.ycord + 1, self.INNER_SQUARE_SIZE, self.INNER_SQUARE_SIZE))


    def select(self):
        """
        Sets the square as selected and draws a blue border around it.
        """

        if not self.selected:
            self.selected = True
            pygame.draw.rect(self.win, constants.BLUE, (self.xcord-1, self.ycord-1, SQUARE_SIZE+1, SQUARE_SIZE+1), 2)

    def deselect(self):
        """
        Deselects the square and returns the outline to what it was before.
        """
        if self.selected:
            self.selected = False

            if self.is_correct == -1:
                pygame.draw.rect(self.win, constants.BLACK, (self.xcord -1 , self.ycord-1, SQUARE_SIZE+1, SQUARE_SIZE+1), 2)
            
            else:
                self.draw_border(self.is_correct)

    def draw_border(self, is_correct):
        """
        Draws the border of the square as green or red depending on if it has the correct value or not.

        Arguments:
            - is_correct: Value of 0 or 1. Pas 1 to draw green border, 0 to draw red.
        """

        self.is_correct = int(is_correct)

        if self.is_correct == 1:
            pygame.draw.rect(self.win, constants.GREEN, (self.xcord -1 , self.ycord-1, SQUARE_SIZE+1, SQUARE_SIZE+1), 2)
        
        elif self.is_correct == 0:
            pygame.draw.rect(self.win, constants.RED, (self.xcord -1 , self.ycord-1, SQUARE_SIZE+1, SQUARE_SIZE+1), 2)

    def remove_border(self):
        """
        Removes correctness check from the square. Border is redrawn as black.
        """

        self.is_correct = -1

        if self.selected:
            pygame.draw.rect(self.win, constants.BLUE, (self.xcord-1, self.ycord-1, SQUARE_SIZE+1, SQUARE_SIZE+1), 2)

        else:
            pygame.draw.rect(self.win, constants.BLACK, (self.xcord -1 , self.ycord-1, SQUARE_SIZE+1, SQUARE_SIZE+1), 2)

