from sudoku_generator import SudokuGenerator


class Sudoku:
    def __init__(self, autogenerate=True, generator=None, solver=None, max_errors=3, max_hints=3, board=None, solution=None):
        self._board = [[0] * 9 for _ in range(9)]
        self._generating_board = True
        self._num_solutions = 0
        self._solver = solver

        self._error_count = 0
        self._max_errors = max_errors
        self._num_hints = 0
        self._max_hints = max_hints
        if autogenerate:
            if generator:
                self._generator = generator
            else:
                self._generator = SudokuGenerator()
            self._board, self._solution = self._generator.generate_game()
        else:
            self._board = board
            if solution:
                self._solution = solution
            else:
                solver.solve(self._board, 0, 0)
                self._solution = solver.get_solved_board()

    def game_won(self):
        for i in range(9):
            for j in range(9):
                if self._board[i][j] != self._solution[i][j]:
                    return False
        return True

    def auto_solve(self):
        self._solver.solve(self._board, 0, 0)
        self._board = self._solver.get_solved_board()

    def play(self, i, j, value):
        if self._solution[i][j] == value:
            self._board[i][j] = value
            return True
        else:
            self._error_count += 1
            if self._error_count >= self._max_errors:
                raise Exception("Game over! You ran out of errors!")
            return False

    def get_hint(self, i, j):
        if self._num_hints < self._max_hints:
            self._board[i][j] = self._solution[i][j]
            self._num_hints += 1
            return self._solution[i][j]

    def get_cell(self, i, j):
        return self._board[i][j]

    def get_board(self):
        return self._board

    def get_solution(self):
        return self._solution

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
