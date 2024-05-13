from sudoku import Sudoku
from graphics import Window
"""
TODO 
implement UI
implement modular improvements to the backtracker (arc consistency, etc)
time in = 6 hours
starting back - 1:30pm
"""

def control(game):
    make_play = lambda args: game.play(*args)
    window = Window(600, 600)
    window.draw(game._board)
    window.add_observer(make_play)
    window.wait_for_close()


def main():
    control(Sudoku())
    # s.auto_solve()
    # window.draw(s._board)
    # for i in range(9):
    #     for j in range(9):
    #         window.update_cell(i, j, 0)
    # print(s)

if __name__ == '__main__':
    main()