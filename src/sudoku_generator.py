from random import randint, seed
from copy import deepcopy
from sudoku_solver import SudokuSolver


class SudokuGenerator:
    def __init__(self, number_of_filled_cells=32, random_seed=None, solver=SudokuSolver(True), template=None):
        if template:
            self.board = template
        else:
            self._board = [
                [3, 1, 6, 5, 7, 8, 4, 9, 2],
                [5, 2, 9, 1, 3, 4, 7, 6, 8],
                [4, 8, 7, 6, 2, 9, 5, 3, 1],
                [2, 6, 3, 4, 1, 5, 9, 8, 7],
                [9, 7, 4, 8, 6, 3, 1, 2, 5],
                [8, 5, 1, 7, 9, 2, 6, 4, 3],
                [1, 3, 8, 9, 4, 7, 2, 5, 6],
                [6, 9, 2, 3, 5, 1, 8, 7, 4],
                [7, 4, 5, 2, 8, 6, 3, 1, 9]
            ]
        self.solver = solver
        self._number_of_filled_cells = number_of_filled_cells
        if random_seed:
            seed(random_seed)

    def _generate_game(self):
        # Then, we make several randomized permutations to the board to create a new solution
        self._shuffle()
        solution = deepcopy(self._board)
        # Finally, we reverse-solve the puzzle until we've reached a puzzle with the specified difficulty.
        self._remove_values()

        # Mark that we've generated the board successfully.
        self._generating_board = False

        # Return the game board
        return self._board, solution

    def _shuffle(self):
        # Shuffle the values in cells randomly
        for i in range(1, 9):
            random_num = randint(1, 9)
            self._swap_numbers(i, random_num)

        # Shuffle the rows
        cell = 0
        for i in range(9):
            random_num = randint(0, 2)
            cell = i // 3
            self._swap_rows(i, cell * 3 + random_num)

        # Shuffle the columns
        for i in range(9):
            random_num = randint(0, 2)
            cell = i // 3
            self._swap_cols(i, cell * 3 + random_num)

        # Shuffle rows as 3x9 chunks
        for i in range(3):
            random_num = randint(0, 2)
            self._shuffle_cells_row(i, random_num)

        # Shuffle cols as 9x3 chunks
        for i in range(3):
            random_num = randint(0, 2)
            self._shuffle_cells_col(i, random_num)

    def _swap_numbers(self, val1, val2):
        for i in range(9):
            for j in range(9):
                if self._board[i][j] == val1:
                    self._board[i][j] = val2
                elif self._board[i][j] == val2:
                    self._board[i][j] = val1

    def _swap_rows(self, row1, row2):
        self._board[row1], self._board[row2] = self._board[row2], self._board[row1]

    def _swap_cols(self, col1, col2):
        for i in range(9):
            self._board[i][col1], self._board[i][col2] = self._board[i][col2], self._board[i][col1]

    def _shuffle_cells_row(self, row1, row2):
        for i in range(3):
            self._swap_rows(row1 * 3 + i, row2 * 3 + i)

    def _shuffle_cells_col(self, col1, col2):
        for i in range(3):
            self._swap_cols(col1 * 3 + i, col2 * 3 + i)

    def _remove_values(self):
        template = deepcopy(self._board)
        board_found = False

        while not board_found:
            # generate a "mask" from the solved template
            keepers = [[0]*9 for _ in range(9)]
            for _ in range(self._number_of_filled_cells):
                x = randint(0, 8)
                y = randint(0, 8)
                while keepers[x][y] != 0:
                    x = randint(0, 8)
                    y = randint(0, 8)
                keepers[x][y] = template[x][y]

            self._board = keepers

            # Attempt to solve the board
            self.solver.solve(self._board, 0, 0)

            # If there's a unique solution, we're done.
            if self.solver._num_solutions == 1:
                board_found = True
            else:
                self.solver._num_solutions = 0
