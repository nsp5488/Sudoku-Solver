from sudoku_generator import SudokuGenerator
from sudoku_solver import SudokuSolver, check_play

class Sudoku:
    def __init__(self, autogenerate=True, generator=None, solver=None):
        self._board = [[0] * 9 for _ in range(9)]
        
        self._generating_board = True
        self._num_solutions = 0
        self._solver = SudokuSolver(False)

        if autogenerate:
            if generator:
                self._generator = generator
            else:
                self._generator = SudokuGenerator()
            self._board = self._generator._generate_game()

    def add_gui(self, window):
        self._window = window
        
        pass
    def auto_solve(self):
        self._solver.solve(self._board, 0, 0)
        self._board = self._solver.get_solved_board()


    def play(self, i, j, value):
        if check_play(self._board, i, j, value):
            self._board[i][j] = value
        else:
            raise Exception("Invalid Play")


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
    