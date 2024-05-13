from sudoku import Sudoku
from sudoku_solver import SudokuSolver
from graphics import Window
"""
TODO 
implement UI
implement modular improvements to the backtracker (arc consistency, etc)
time in = 6 hours
starting back - 1:30pm
"""

def main():
    s = Sudoku(True)
    window = Window(600, 600)
    window.draw(s._board)
    # s.auto_solve()
    # window.draw(s._board)
    # for i in range(9):
    #     for j in range(9):
    #         window.update_cell(i, j, 0)
    # print(s)
    window.wait_for_close()

if __name__ == '__main__':
    main()