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

        self.correct_solution = np.array([[5, 6, 8, 9, 1, 3, 4, 2, 7],
                                    [1, 9, 7, 2, 5, 4, 6, 8, 3],
                                    [3, 4, 2, 6, 8, 7, 9, 1, 5],
                                    [6, 8, 5, 4, 7, 9, 1, 3, 2],
                                    [7, 3, 4, 1, 6, 2, 5, 9, 8],
                                    [2, 1, 9, 5, 3, 8, 7, 6, 4],
                                    [9, 2, 6, 3, 4, 5, 8, 7, 1],
                                    [8, 5, 1, 7, 2, 6, 3, 4, 9],
                                    [4, 7, 3, 8, 9, 1, 2, 5, 6]])


        self.sudoku_solver_test = SudokuSolver(self.test_matrix)

    def test_canary(self):
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

    # def test_matrix_invalid_dtype_throws_exception(self):
    #     pass

    # def test_matrix_non_numeric(self):
    #     pass

    def test_get_submatrix_coord(self):
        assert self.sudoku_solver_test.get_submatrix_coord(3, 2) == (3, 0)

    def test_element_is_valid(self):
        assert self.sudoku_solver_test.is_valid_element(2, 1, 1) == True

    def test_invalid_num_in_row(self):
        assert self.sudoku_solver_test.is_valid_element(4, 1, 1) == False

    def test_invalid_num_in_col(self):
        assert self.sudoku_solver_test.is_valid_element(7, 1, 1) == False

    def test_invalid_num_in_submatrix(self):
        assert self.sudoku_solver_test.is_valid_element(1, 0, 2) == False

    def test_next_loc(self):
        i, j = 0, 5

        next_i, next_j = self.sudoku_solver_test.next_loc(i, j)
        assert next_i == 0 and next_j == 6

    def test_next_loc_end_row(self):
        i, j = 1, 8
        
        next_i, next_j = self.sudoku_solver_test.next_loc(i, j)
        assert next_i == 2 and next_j == 0

    def test_next_loc_next_elem_not_empty(self):
        i, j = 3, 0

        next_i, next_j = self.sudoku_solver_test.next_loc(i, j)
        assert next_i == 3 and next_j == 3

    def test_next_loc_empty(self):
        i, j = 0, 0

        next_i, next_j = self.sudoku_solver_test.next_loc(i, j)
        assert next_i == 0 and next_j == 0

    def test_next_loc_at_end(self):
        filled_solver = SudokuSolver(self.correct_solution)

        next_i, next_j = filled_solver.next_loc(8, 8)
        assert next_i == 9 and next_j == 0

    def test_correct_solution(self):
        result = self.sudoku_solver_test.solve()
        
        assert result == True
        assert np.array_equal(self.sudoku_solver_test.matrix, self.correct_solution)

    def test_solution_passing_correct_filled_matrix(self):
        correct_filled_solver = SudokuSolver(self.correct_solution)

        assert correct_filled_solver.solve() == True

    def test_solution_passing_incorrect_filled_matrix(self):
        incorrect_filled_solver = SudokuSolver(np.ones((9, 9)))
        assert incorrect_filled_solver.solve() == False

    def test_solution_with_invalid_starting_nums(self):
        # Invalid starting entry in position 0,8
        invalid_matrix = np.array([[0, 0, 0, 0, 0, 3, 0, 2, 3],
                                    [1, 0, 0, 0, 0, 4, 6, 0, 3],
                                    [0, 0, 0, 6, 0, 0, 0, 1, 0],
                                    [6, 8, 5, 0, 7, 0, 1, 3, 2],
                                    [7, 0, 0, 1, 6, 0, 5, 0, 8],
                                    [0, 1, 9, 5, 0, 0, 0, 0, 4],
                                    [9, 0, 0, 0, 4, 0, 0, 7, 1],
                                    [0, 0, 0, 7, 2, 6, 0, 0, 0],
                                    [0, 7, 3, 8, 9, 1, 0, 5, 0]])

        incorrect_matrix_solver = SudokuSolver(invalid_matrix)
        assert incorrect_matrix_solver.solve() == False

    def test_solution_is_found_with_empty_starting_matrix(self):
        empty_matrix_solver = SudokuSolver(np.zeros((9, 9)))
        assert empty_matrix_solver.solve() == True

    # def test_solution_when_matrix_has_no_solution(self):
    #     pass

    # def test_solution_matrix_with_nonempty_first_element(self):
    #     pass





