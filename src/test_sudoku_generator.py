import unittest

from sudoku_generator import SudokuGenerator
from sudoku_solver import SudokuSolver, check_play


class TestSudokuGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = SudokuGenerator(number_of_filled_cells=32, random_seed=0, solver=SudokuSolver(True, False, 0, True, True))
        return super().setUp()

    def test_board_generation(self):
        board, solution = self.generator._generate_game()

        for i in range(9):
            for j in range(9):
                value = board[i][j]  # Cache the true value
                if value != 0:
                    board[i][j] = 0  # Reset the value
                    # Assert that that value results in a valid board
                    self.assertTrue(check_play(board, i, j, value))
