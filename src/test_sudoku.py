import unittest
from sudoku import Sudoku

class TestSudoku(unittest.TestCase):
    def setUp(self) -> None:
        self.puzzle = Sudoku()

        return super().setUp()

    def test_play(self):
        p1 = (0, 0, 1)
        self.puzzle.play(*p1)
        self.assertEqual(1, self.puzzle.get_cell(0, 0))

    def test_check_play_row(self):
        p1 = (0, 0, 1)
        p2 = (0, 5, 1)
        self.puzzle.play(*p1)
        self.assertRaises(Exception, self.puzzle.play, p2)


    def test_check_play_col(self):
        p1 = (0, 0, 1)
        p2 = (5, 0, 1)
        self.puzzle.play(*p1)
        self.assertRaises(Exception, self.puzzle.play, p2)

    def test_check_play_cell(self):
        p1 = (0, 0, 1)
        p2 = (1, 1, 1)
        self.puzzle.play(*p1)
        self.assertRaises(Exception, self.puzzle.play, p2)

