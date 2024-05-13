from sudoku_generator import SudokuGenerator
from sudoku_solver import SudokuSolver, check_play

class Sudoku:
    def __init__(self, autogenerate=True, generator=None, solver=None, max_errors=3):
        self._board = [[0] * 9 for _ in range(9)]
        self._error_count = 0
        self._generating_board = True
        self._num_solutions = 0
        self._solver = SudokuSolver(False)
        self._max_errors = max_errors
        if autogenerate:
            if generator:
                self._generator = generator
            else:
                self._generator = SudokuGenerator()
            self._board = self._generator._generate_game()


    def auto_solve(self):
        self._solver.solve(self._board, 0, 0)
        self._board = self._solver.get_solved_board()


    def play(self, i, j, value):
        if check_play(self._board, i, j, value):
            self._board[i][j] = value
            return True
        else:
            self._error_count += 1
            if self._error_count >= self._max_errors:
                raise Exception("Game over! You ran out of errors!")
            return False


    def get_cell(self, i, j):
        return self._board[i][j]


    def __repr__(self):
        out = ''

        for i, row in enumerate(self._board):
            if i % 3 == 0:
                out += '\n' + '-'*13 + '\n'
            else:
                out += '\n'
            
            for j, cell in enumerate(row):
                if j % 3 == 0:
                    out += '|'

                if cell:
                    out += str(cell)
                else:
                    out += ' '
            out += '|'

        out += '\n' + '-'*13 
        return out       
    