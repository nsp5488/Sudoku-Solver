class SudokuGenerator:
    def __init__(self, cells_to_fill):
        self.cells_to_fill = cells_to_fill
        self.board = [[None] for _ in range(9)]

    