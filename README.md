# Sudoku Solver: Project Overview
* Text-based and GUI sudoku solver programs which use a backtracking algorithm to solve a sudoku puzzle.
* Unit tests written for the text-based version of the program.
* GUI allows user to play the sudoku game normally and check whether each square is correct.

## Python Packages Used
* NumPy, PyGame, PyTest
* To install dependencies: pip install -r requirements.txt

## File overview
* Text-based solver: sudoku_solver.py
  * Outputs solution of puzzle on the console.
* Unit tests for text-based solver: sudoku_solver_test.py
  * To run unit tests, use command: pytest
* GUI solver: board.py, square.py, constants.py

## How to Play
* Run board.py with command: python board.py
* Click any square to select it (outline in blue) and then type a number between 1-9 to enter that number
* Move selected square with arrow keys
* Right click square to see if inputted number is correct (green border) or not (red border). Right click again to remove correctness check (ie, play the game without any help)
* Delete key will remove inputted number from selected square
* Pressing R clears the board back to beginning state
* Pressing space bar will solve the puzzle with a backtracking algorithm at a slowed down speed in order to get a visual depiction of the algorithm. A sample solve is seen below:


[![Image from Gyazo](https://i.gyazo.com/198a90e152d286dc49540b87fd0f310d.gif)](https://gyazo.com/198a90e152d286dc49540b87fd0f310d)
