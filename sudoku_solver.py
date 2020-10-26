import numpy as np

class SudokuSolver:

    def __init__(self, matrix):
        self.set_matrix(matrix)

    def set_matrix(self, matrix):
        """
        Sets the Sudoku matrix if it is valid type. Use 0 to represent empty squares.
        Matrix is set to None if it is not of valid shape and contents.
        """
        try:
            matrix = matrix.astype('int32')
            self.matrix = matrix if self.is_valid_matrix(matrix) else None

        except AttributeError:
            # Handle if matrix is a list
            matrix = np.array(matrix, dtype=np.int32)
            self.matrix = matrix if self.is_valid_matrix(matrix) else None

    def is_valid_matrix(self, matrix):
        """
        Returns True if matrix is 9x9 and only contains numbers between 0 and 9.
        """
        return self.is_9x9(matrix) and self.is_valid_nums(matrix)

    def is_9x9(self, matrix):
        """
        Returns True if matrix is 9x9.
        """
        return matrix.ndim == 2 and matrix.shape == (9, 9)

    def is_valid_nums(self, matrix):
        """
        Returns True if matrix only contains numbers 0 to 9 (0 represents empty square).
        """
        return matrix[(matrix < 0) | (matrix > 9)].sum() == 0

    def set_num(self, num, row, col):
        """
        Sets num at position (row, col). Num must be between 0 - 9 (0 represents empty).
        """
        if num >= 0 and num <=9:
            self.matrix[row, col] = int(num)
                
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
        for j in range(self.matrix.shape[1]):
            if j != col and self.matrix[row, j] == num:
                return False
        
        # Check if duplicate in col
        for i in range(self.matrix.shape[0]):
            if i != row and self.matrix[i, col] == num:
                return False

        # Check if duplicate in submatrix
        submatrix_loc = self.get_submatrix_coord(row, col)

        for i in range(submatrix_loc[0], submatrix_loc[0] + 3):
            for j in range(submatrix_loc[1], submatrix_loc[1] + 3):
                if (i, j) != (row, col) and self.matrix[i, j] == num:
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

        while next_i < 9 and next_j < 9 and self.matrix[next_i, next_j] != 0:
            next_i = next_i if next_j < 8 else next_i + 1
            next_j = next_j + 1 if next_j < 8 else 0

        return next_i, next_j

    def is_final_solution(self):
        """
        Returns True if every element is valid. Should only be used to check condition of the final filled matrix.
        Will return False if matrix contains any empty elements.
        """
        
        if 0 in self.matrix:
            return False

        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                if not self.is_valid_element(self.matrix[i, j], i, j):
                    return False

        return True

    def find_solution(self, i, j):
        """
        Recursive backtracking algorithm to find a valid solution for the Sudoku matrix.
        Returns True if a solution is found.
        """

        # Base case
        if 0 not in self.matrix:
            # Only need to check full validity if no empty cells are present (like in case that Solver is passed a bad full matrix)
            # Otherwise algorithm will ensure validity at all steps
            return self.is_final_solution()

        else:
            num = 1
            is_solution = False

            while num < 10 and not is_solution:
                # Check if num is valid in position (i,j)
                if self.is_valid_element(num, i, j):
                    self.set_num(num, i, j)
                
                    # Determine next position to fill
                    next_i, next_j = self.next_loc(i, j)

                    # Recursivly see if this leads to a solution.
                    is_solution = self.find_solution(next_i, next_j)
    
                num += 1

            # Reset to 0 (empty) if all numbers tried and no solution in this path
            if not is_solution:
                self.set_num(0, i, j)
                
            return is_solution

    def solve(self):
        """
        Solves the Sudoku matrix, and returns the solution as numpy array. Solution can be accessed in matrix attribute.
        """
        start_i, start_j = self.next_loc(0, 0)
        has_solution = self.find_solution(start_i, start_j)

        return self.matrix if has_solution else None


if __name__ == '__main__':
    matrix = np.array([[1, 0, 0, 0, 8, 4, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 6, 0, 0],
                        [0, 0, 0, 0, 9, 0, 0, 0, 0],
                        [4, 0, 0, 7, 0, 0, 0, 8, 0],
                        [3, 0, 0, 4, 0, 0, 0, 6, 0],
                        [5, 0, 1, 0, 2, 8, 0, 7, 3],
                        [0, 0, 0, 6, 0, 0, 0, 0, 5],
                        [0, 0, 7, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 5, 4, 0, 0, 0, 8]])

    solver = SudokuSolver(matrix)
    solution = solver.solve()
    print("The found solution was: ")
    print(solution)
