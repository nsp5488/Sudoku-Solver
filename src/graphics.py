from tkinter import Tk, Frame, StringVar, Entry

class Window:
    def __init__(self, width, height):
        self._root = Tk()
        self._root.title = "Sudoku"
        self._board = Frame(self._root, bg='white')
        self._board.pack()

        self._running = False
        self._contents = [[None]*9 for _ in range(9)]
        self._cells = [[None]*9 for _ in range(9)]
        self._build_cells()

        self._root.protocol("WM_DELETE_WINDOW", self.close)


    def _build_cells(self):
        frames = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                frames[i][j] = Frame(self._board, bd=1, highlightbackground='black', highlightthickness=1)
                frames[i][j].grid(row=i, column=j, sticky='nsew')

        self._cells = [[None]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                cell = Frame(frames[i//3][j//3])
                cell.grid(row=i%3, column=j%3, sticky='nsew')
                self._contents[i][j] = StringVar(name=f'{i},{j}')
                self._cells[i][j] = Entry(cell, bg='white', width=3, textvariable=self._contents[i][j], justify='center', foreground='black')
                self._cells[i][j].grid(sticky='nsew')

                self._contents[i][j].trace_add("write", self._handle)
                self._contents[i][j].trace_add("unset", self._handle)

                
    def _handle(self, name, handle, op):
        indices = name.split(',')
        i, j = int(indices[0]), int(indices[1])
        contents = self._contents[i][j].get()
        # print(f"{op} to ({i},{j}) with value {contents}")

    def draw(self, board):
        print("Drawing initial board...")
        for i in range(9):
            for j in range(9):
                value = board[i][j]
                self.update_cell(i, j, value)

                if self._contents[i][j].get() != ' ':
                    self._cells[i][j].configure(state='disabled')
                self.redraw()

    def update_cell(self, i, j, value, error=False):
        label = self._contents[i][j]
        if value:
            value = f"{value}"
        else:
            value = ' '
        label.set(value)
        if error:
            self._cells[i][j].configure(foreground='red')
        else:
            self._cells[i][j].configure(foreground='black')
        
        self.redraw()

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self._running = True
        while self._running:
            self.redraw()

    def close(self):
        self._running = False
