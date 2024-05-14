import time
class SudokuSolver:
    def __init__(self, generating_board=False, visualize=False, visualize_timer=0.05):
        self._generating_board = generating_board
        self._num_solutions = 0
        self._board = []
        self._visualize = visualize
        self._vis_update = None
        self._visualize_timer = visualize_timer
        
    def solve(self, board, row, col):
        self._board = board
        return self._fill_board(row, col)

    def get_solved_board(self):
        return self._board

    def set_visualize_display(self, vis_update):
        self._vis_update = vis_update


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
            if self._visualize:
                self._vis_update((row, col, value, not check_play(self._board, row, col, value)))
                time.sleep(self._visualize_timer)
            if check_play(self._board, row, col, value):
                self._board[row][col] = value
                if self._fill_board(row, col + 1):
                    return True
            if self._visualize:
                self._vis_update((row, col, 0))
            self._board[row][col] = 0

        return False

"""
Utitlity method to check if a play is valid given a board, location, and value to play.
"""
def check_play(board, i, j, value) -> bool:
    # Check bounds
    if i < 0 or i >= 9 or j < 0 or j >= 9 or value < 1 or value > 9:
        return False

    # Check for duplicates in row / column        
    for y in range(len(board)):
        if board[y][j] == value:
            return False
        if board[i][y] == value:
            return False
        
    # Check for duplicates in 3x3 cell
    cell_row = i - i % 3 # These represent the top left coordinate of the cell
    cell_col = j - j % 3
    for x in range(cell_row, cell_row + 3):
        for y in range(cell_col, cell_col + 3):
            if board[x][y] == value:
                return False
            
    return True