

class Sudoku:
    def __init__(self):
        self._board = [[None] * 9 for _ in range(9)]

    def play(self, i, j, value):
        if self._check_play(i, j, value):
            self._board[i][j] = value
        else:
            raise Exception("Invalid Play")

    def _check_play(self, i, j, value) -> bool:
        # Check bounds
        if i < 0 or i >= 9 or j < 0 or j >= 9 or self._board[i][j] != None:
            print("bounds")
            return False
        
        # Check for duplicates in row / column
        if value in self._board[i]:
            return False
        
        for y in range(len(self._board)):
            if self._board[y][j] == value:
                return False
            
        # Check for duplicates in 3x3 cell
        cell_row = i // 3 # These represent the top left coordinate of the cell
        cell_col = j // 3
        for x in range(cell_row, cell_row + 3):
            for y in range(cell_col, cell_col + 3):
                if self._board[x][y] == value:
                    return False
                
        return True


    def get_cell(self, i, j):
        return self._board[i][j]


    def fill_board(self):
        i = 0
        j = 0
        k = 1
        while i < 9:
            if self._check_play(i, j, k):
                self._board[i][j] = k
                j += 1
                i += int(j / 9)
                j = j % 9
                k = 1
            else:
                k += 1
                
                
            
    def _generate_game(self):
        pass

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