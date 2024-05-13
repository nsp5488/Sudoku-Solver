from sudoku import Sudoku
"""
TODO 
implement UI
implement modular improvements to the backtracker (arc consistency, etc)
time in = 5 hours
"""

def main():
    s = Sudoku(30)
    print(s)
    s._fill_board(0,0)
    print(s)

if __name__ == '__main__':
    main()