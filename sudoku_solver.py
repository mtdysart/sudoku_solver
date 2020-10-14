import numpy as np

class SudokuSolver:

    def __init__(self, matrix):
        self.set_matrix(matrix)

    def set_matrix(self, matrix):
        """
        Sets the Sudoku matrix if it is valid. Use 0 to represent empty squares.
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
        return matrix.ndim == 2 and matrix.shape[0] == 9 and matrix.shape[1] == 9

    def is_valid_nums(self, matrix):
        """
        Returns True if matrix only contains numbers 0 to 9 (0 represents empty square).
        """
        return matrix[(matrix < 0) | (matrix > 9)].sum() == 0

    # def is_duplicate_free(self, matrix):
    #     """
    #     Returns True if matrix has no invalid duplicates. 
    #     """
    #     for i in matrix.shape[0]:
    #         for j in matrix.shape[1]:
    #             if matrix[i, j] > 0 and not self.is_valid_element(matrix[i, j], i, j):
    #                 return False

    #     return True
                    
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
        Returns a tuple for the next empty location to check. Order is left to right. 
        """
        next_i, next_j = i, j

        while next_i < 9 and next_j < 9 and self.matrix[next_i, next_j] != 0:
            next_i = next_i if next_j < 8 else next_i + 1
            next_j = next_j + 1 if next_j < 8 else 0

        return next_i, next_j


    def find_solution(self, i, j):
        # Base case
        if 0 not in self.matrix:
            return True

        else:
            num = 1
            is_solution = False

            while num < 10 and not is_solution:
                # Check if num is valid in position (i,j)
                if self.is_valid_element(num, i, j):
                    self.matrix[i, j] = num
                
                    # Determine next position to fill
                    next_i, next_j = self.next_loc(i, j)

                    # Recursivly see if this leads to a solution.
                    is_solution = self.find_solution(next_i, next_j)
    
                num += 1

                # Reset to 0 if all numbers tried and no solution in this path
                if num == 10 and not is_solution:
                    self.matrix[i, j] = 0
                
            
            return is_solution

    def solve(self):
        start_i, start_j = self.next_loc(0, 0)
        has_solution = self.find_solution(start_i, start_j)

        if has_solution:
            print("A solution was found:")
            print(self.matrix)

        else:
            print("This matrix has no solution.")



