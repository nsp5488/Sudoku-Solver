from copy import deepcopy
import random
class Sudoku:
    def __init__(self, number_of_filled_cells=32, random_seed=None):
        self._board = [[0] * 9 for _ in range(9)]
        
        self._generating_board = True
        self._num_solutions = 0
        self._number_of_filled_cells = number_of_filled_cells
        if random_seed:
            random.seed(random_seed)


    def play(self, i, j, value):
        if self._check_play(i, j, value):
            self._board[i][j] = value
        else:
            raise Exception("Invalid Play")


    def get_cell(self, i, j):
        return self._board[i][j]
   

    def _check_play(self, i, j, value) -> bool:
        # Check bounds
        if i < 0 or i >= 9 or j < 0 or j >= 9:
            return False

        # Check for duplicates in row / column        
        for y in range(len(self._board)):
            if self._board[y][j] == value:
                return False
            if self._board[i][y] == value:
                return False
            
        # Check for duplicates in 3x3 cell
        cell_row = i - i % 3 # These represent the top left coordinate of the cell
        cell_col = j - j % 3
        for x in range(cell_row, cell_row + 3):
            for y in range(cell_col, cell_col + 3):
                if self._board[x][y] == value:
                    return False
                
        return True


    def _fill_board(self, row, col):
        if self._generating_board and self._num_solutions > 1:
                return False
        if row == 8 and col == 9:
            self._num_solutions += 1
            return not self._generating_board
        if col == 9:
            col = 0
            row = row + 1
        

        if self._board[row][col] > 0:
            return self._fill_board(row, col + 1)
        
        for value in range(1, 10):
            if self._check_play(row, col, value):
                self._board[row][col] = value
                if self._fill_board(row, col + 1):
                    return True
        
            self._board[row][col] = 0

        return False


    def _generate_game(self):
        # We begin with a solved board as a template
        self._board = [
        [3,1,6,5,7,8,4,9,2],
        [5,2,9,1,3,4,7,6,8],
        [4,8,7,6,2,9,5,3,1],
        [2,6,3,4,1,5,9,8,7],
        [9,7,4,8,6,3,1,2,5],
        [8,5,1,7,9,2,6,4,3],
        [1,3,8,9,4,7,2,5,6],
        [6,9,2,3,5,1,8,7,4],
        [7,4,5,2,8,6,3,1,9]
        ]

        # Then, we make several randomized permutations to the board to create a new solution
        self._shuffle()

        # Finally, we reverse-solve the puzzle until we've reached a puzzle with the specified difficulty.
        self._remove_values()
        
        # Mark that we've generated the board successfully.
        self._generating_board = False


    def _shuffle(self):
        # Shuffle the values in cells randomly
        for i in range(1, 9):
            random_num = random.randint(1, 9)
            self._swap_numbers(i, random_num)

        # Shuffle the rows
        cell = 0
        for i in range(9):
            random_num = random.randint(0, 2)
            cell = i // 3
            self._swap_rows(i, cell * 3 + random_num)
        
        # Shuffle the columns
        for i in range(9):
            random_num = random.randint(0,2)
            cell = i // 3
            self._swap_cols(i, cell * 3 + random_num)

        # Shuffle rows as 3x9 chunks
        for i in range(3):
            random_num = random.randint(0,2)
            self._shuffle_cells_row(i, random_num)
        
        # Shuffle cols as 9x3 chunks
        for i in range(3):
            random_num = random.randint(0,2)
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
                x = random.randint(0, 8)
                y = random.randint(0, 8)
                while keepers[x][y] != 0:
                    x = random.randint(0, 8)
                    y = random.randint(0, 8)   
                keepers[x][y] = template[x][y]

            
            self._board = keepers

            # Attempt to solve the board
            self._fill_board(0,0)

            # If there's a unique solution, we're done.
            if self._num_solutions == 1:
                board_found = True
            else:
                self._num_solutions = 0


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
