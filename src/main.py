from sudoku import Sudoku
from graphics import Window
"""
TODO 
implement UI:
    number of errors,
    solve button w/ animated solve
implement modular improvements to the backtracker (arc consistency, etc)
time in = 10 hours
"""

def control(game):
    make_play = lambda args: game.play(*args)
    window = Window(600, 600)
    window.draw(game._board)
    window.add_observer(make_play)
    window.wait_for_close()


def main():
    print("Generating puzzle...")
    control(Sudoku())
    # s.auto_solve()
    # window.draw(s._board)
    # for i in range(9):
    #     for j in range(9):
    #         window.update_cell(i, j, 0)
    # print(s)

if __name__ == '__main__':
    main()