import unittest

from sudoku_generator import SudokuGenerator
from sudoku_solver import check_play

class TestSudokuGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = SudokuGenerator(32, 0)
        return super().setUp()
    

    def test_board_generation(self):
        board, solution = self.generator._generate_game()

        for i in range(9):
            for j in range(9):
                value = board[i][j] # Cache the true value
                if value != 0:
                    board[i][j] = 0 # Reset the value
                    self.assertTrue(check_play(board, i, j, value)) # Assert that that value results in a valid board
