from sudoku_solver import SudokuSolver
import numpy as np
import pytest

class TestSudokuSolver:

    def setup_method(self):
        self.test_matrix = np.array([[0, 0, 0, 0, 0, 3, 0, 2, 7],
                                    [1, 0, 0, 0, 0, 4, 6, 0, 3],
                                    [0, 0, 0, 6, 0, 0, 0, 1, 0],
                                    [6, 8, 5, 0, 7, 0, 1, 3, 2],
                                    [7, 0, 0, 1, 6, 0, 5, 0, 8],
                                    [0, 1, 9, 5, 0, 0, 0, 0, 4],
                                    [9, 0, 0, 0, 4, 0, 0, 7, 1],
                                    [0, 0, 0, 7, 2, 6, 0, 0, 0],
                                    [0, 7, 3, 8, 9, 1, 0, 5, 0]])

        self.sudoku_solver_test = SudokuSolver(self.test_matrix)

    def test_true(self):
        assert True

    def test_set_matrix(self):
        assert self.sudoku_solver_test.matrix is not None

    def test_set_matrix_list(self):
        test_matrix_list = list(self.test_matrix)
        solver_test_list = SudokuSolver(test_matrix_list)

        assert solver_test_list.matrix is not None

    def test_matrix_not_9x9(self):
        solver_not_9x9 = SudokuSolver(np.zeros((8, 8)))

        assert solver_not_9x9.matrix is None

    def test_matrix_invalid_nums(self):
        matrix_invalid_nums = np.where(self.test_matrix == 9, 10, self.test_matrix)
        solver_invalid_nums = SudokuSolver(matrix_invalid_nums)

        assert solver_invalid_nums.matrix is None

    # def test_matrix_non_numeric(self):
    #     pass

    # def test_matrix_not_array(self):
    #     pass

    # def test_matrix_with_duplicates(self):
    #     pass

    def test_next_loc(self):
        i, j = 0, 5

        next_i, next_j = self.sudoku_solver_test.next_loc(i, j)
        assert next_i == 0 and next_j == 6

    def test_next_loc_end_row(self):
        i, j = 1, 8
        
        next_i, next_j = self.sudoku_solver_test.next_loc(i, j)
        assert next_i == 2 and next_j == 0

    def test_next_loc_not_empty(self):
        i, j = 3, 0

        next_i, next_j = self.sudoku_solver_test.next_loc(i, j)
        assert next_i == 3 and next_j == 3

    def test_next_loc_empty(self):
        i, j = 0, 0

        next_i, next_j = self.sudoku_solver_test.next_loc(i, j)
        assert next_i == 0 and next_j == 0

    def test_correct_solution(self):
        correct_solution = np.array([[5, 6, 8, 9, 1, 3, 4, 2, 7],
                                    [1, 9, 7, 2, 5, 4, 6, 8, 3],
                                    [3, 4, 2, 6, 8, 7, 9, 1, 5],
                                    [6, 8, 5, 4, 7, 9, 1, 3, 2],
                                    [7, 3, 4, 1, 6, 2, 5, 9, 8],
                                    [2, 1, 9, 5, 3, 8, 7, 6, 4],
                                    [9, 2, 6, 3, 4, 5, 8, 7, 1],
                                    [8, 5, 1, 7, 2, 6, 3, 4, 9],
                                    [4, 7, 3, 8, 9, 1, 2, 5, 6]])

        result = self.sudoku_solver_test.find_solution(0, 0)
        
        assert result == True
        assert np.array_equal(self.sudoku_solver_test.matrix, correct_solution)



