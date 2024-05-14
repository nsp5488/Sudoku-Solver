import unittest

from sudoku_solver import SudokuSolver, check_play


class TestSudokuSolver(unittest.TestCase):
    def setUp(self) -> None:
        self.solver = SudokuSolver()
        self.board = [
        [7, 0, 1, 6, 0, 0, 5, 0, 0],
        [0, 0, 2, 0, 8, 0, 0, 7, 0],
        [0, 6, 0, 7, 2, 0, 0, 1, 9],
        [0, 4, 0, 1, 6, 7, 0, 0, 8],
        [6, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9, 4, 0, 0, 0, 0],
        [8, 2, 0, 0, 0, 9, 0, 5, 0],
        [4, 3, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 8, 0, 2, 9, 4, 0]] 
        return super().setUp()

    def test_solve(self):
        
        self.assertTrue(self.solver.solve(self.board, 0, 0))
        solution = self.solver.get_solved_board()
        for i in range(9):
            for j in range(9):
                value = solution[i][j] # Cache the true value
                if value != 0:
                    solution[i][j] = 0 # Reset the value
                    self.assertTrue(check_play(solution, i, j, value)) # Assert that that value results in a valid board


    def test_check_play_row(self):
        self.assertFalse(check_play(self.board, 0, 1, 5))


    def test_check_play_col(self):
        self.assertFalse(check_play(self.board, 0, 1, 6))

    def test_check_play_cell(self):
        self.assertFalse(check_play(self.board, 0, 1, 1))
