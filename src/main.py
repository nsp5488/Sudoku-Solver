from sudoku import Sudoku
from graphics import Window
from sudoku_solver import SudokuSolver
"""
TODO 
implement UI:
implement modular improvements to the backtracker (arc consistency, etc)
time in = 10 hours
resume @ 7pm
"""

def control(game, window):
    make_play = lambda args: game.play(*args)
    solve_callback = lambda: game._solver.solve(game._board, 0, 0)
    
    window.set_max_errors(3)
    window.draw(game._board)

    window.add_observer(make_play)
    window.set_solve_callback(solve_callback)
    # game._solver.solve(game._board, 0, 0)
    window.wait_for_close()


def main():
    print("Generating puzzle...")
    window = Window(600, 600)
    solver = SudokuSolver(visualize=True)
    solver.set_visualize_display(vis_update = lambda args: window.update_cell(*args))
    game = Sudoku(solver=solver)
    
    control(game, window)
    # s.auto_solve()
    # window.draw(s._board)
    # for i in range(9):
    #     for j in range(9):
    #         window.update_cell(i, j, 0)
    # print(s)

if __name__ == '__main__':
    main()