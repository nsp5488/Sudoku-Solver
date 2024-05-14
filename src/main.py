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
    def make_play(args): return game.play(*args)
    def view_solution_callback(): return window.draw(game.get_solution())

    window.set_max_errors(3)
    window.draw(game.get_board())

    window.set_win_condition(game.game_won)
    window.add_observer(make_play)
    window.set_solve_callback(game.auto_solve)
    window.set_view_solution_callback(view_solution_callback)

    window.wait_for_close()


def main():
    print("Generating puzzle...")
    window = Window(600, 600)
    solver = SudokuSolver(visualize=True, visualize_timer=.05, use_forward_checking=False)
    solver.set_visualize_display(
        vis_update=lambda args: window.update_cell(*args))
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
