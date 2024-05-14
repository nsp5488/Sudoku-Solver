import unittest

from sudoku_generator import SudokuGenerator
from sudoku_solver import SudokuSolver, check_play


class TestSudokuGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = SudokuGenerator(number_of_filled_cells=17, random_seed=1, solver=SudokuSolver(True, False, 0, True, True))
        return super().setUp()

    def test_board_generation(self):
        board, solution = self.generator._generate_game()
        num_filled = 0
        for i in range(9):
            for j in range(9):
                value = board[i][j]  # Cache the true value
                if value != 0:
                    board[i][j] = 0  # Reset the value
                    # Assert that that value results in a valid board
                    self.assertTrue(check_play(board, i, j, value))
                    num_filled += 1

        self.assertEqual(32, num_filled)
        
