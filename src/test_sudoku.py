import unittest
from sudoku import Sudoku

class TestSudoku(unittest.TestCase):
    def setUp(self) -> None:
        self.puzzle = Sudoku(False, None, None, 3, [[0, 2], [0, 0]], [[1, 2], [3, 4]])

        return super().setUp()

    def test_play(self):
        p1 = (0, 0, 1)
        self.puzzle.play(*p1)
        self.assertEqual(1, self.puzzle.get_cell(0, 0))

