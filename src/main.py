from sudoku import Sudoku
from graphics import GameWindow, MenuWindow
from sudoku_solver import SudokuSolver
from sudoku_generator import SudokuGenerator


def control(game, window):
    def make_play(args): return game.play(*args)

    print("Drawing the board...")
    window.draw(game.get_board())

    # This enables the "rules", adding it after drawing the initial board saves us some performance
    window.set_play_callback(make_play)

    window.wait_for_close()


def main():
    menu = MenuWindow()
    options = menu.start()
    use_ac3 = options['solver_type'] > 1
    use_mrv = options['solver_type'] > 2
    use_forward_check = options['solver_type'] > 3
    if not options['start']:
        return
    
    print("Generating puzzle...")
    solver = SudokuSolver(visualize=options['visualize'], visualize_timer=options['timer'], use_ac3=use_ac3,
                          use_mrv=use_mrv, use_forward_checking=use_forward_check)
    generator = SudokuGenerator(options['difficulty'])

    game = Sudoku(solver=solver, max_errors=options['num_errors'],
                  max_hints=options['num_hints'], generator=generator)

    print("Building game window...")
    window = GameWindow()
    def view_solution_callback(): return window.draw(game.get_solution())

    window.set_max_errors(options['num_errors'])
    window.set_max_hints(options['num_hints'])
    window.set_hint_callback(lambda args: game.get_hint(*args))
    window.set_win_condition(game.game_won)
    window.set_solve_callback(game.auto_solve)
    window.set_view_solution_callback(view_solution_callback)

    # This enables the model to update the GUI easily
    solver.set_visualize_display(
        vis_update=lambda args: window.update_cell(*args))

    control(game, window)


if __name__ == '__main__':
    main()
