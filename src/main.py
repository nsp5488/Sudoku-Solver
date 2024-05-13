from sudoku import Sudoku
from sudoku_solver import SudokuSolver
"""
TODO 
implement UI
implement modular improvements to the backtracker (arc consistency, etc)
time in = 6 hours
starting back - 1:30pm
"""

def main():
    s = Sudoku(True)
    print(s)
    s.auto_solve()
    print(s)

if __name__ == '__main__':
    main()