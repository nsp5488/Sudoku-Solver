from tkinter import Tk, Frame, StringVar, Entry, Label, Button

class Window:
    def __init__(self, width, height, observers = []):
        self._root = Tk()
        self._root.title = "Sudoku"

        self._board = Frame(self._root, bg='white')
        self._board.grid(row=0, rowspan=9)
        # self._board.pack()

        self._bottom_frame = Frame(self._root)
        self._bottom_frame.grid(row=10)
        self._error_label = Label(self._bottom_frame)
        self._error_label.grid(row = 0, column=1)
        self._num_errors = 0
        self.max_errors = 3
        self._disable_game = False

        self._solve_button = Button(self._bottom_frame, text="Solve")
        self._solve_button.grid(row=0, column=0)


        self._observers = observers

        self._running = False
        self._contents = [[None]*9 for _ in range(9)]
        self._cells = [[None]*9 for _ in range(9)]
        self._build_cells()

        self._root.protocol("WM_DELETE_WINDOW", self.close)

    def set_solve_callback(self, solve_func):
        self._solve_button.configure(command=lambda:[self.disable_game(), solve_func()])

    def set_max_errors(self, max_errors):
        self.max_errors = max_errors
        self._error_label.configure(text=f"Errors: {self._num_errors}/{self.max_errors}")

    def add_observer(self, observer):
        self._observers.append(observer)


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
                self._cells[i][j] = Entry(cell, bg='white', width=3, textvariable=self._contents[i][j], 
                                          justify='center', foreground='black', )
                self._cells[i][j].grid(sticky='nsew')

                self._contents[i][j].trace_add("write", self._handle)

    def disable_game(self):
        self._disable_game = True
                
    def _handle(self, name, handle, op):
        if self._disable_game:
            return
        indices = name.split(',')
        i, j = int(indices[0]), int(indices[1])
        contents_str = self._contents[i][j].get().strip()
        if contents_str.isnumeric():
            contents = int(contents_str)
        else:
            self._cells[i][j].configure(foreground="red")
            return
        for observer in self._observers:
            args = (i, j, contents)
            try:
                result = observer(args)
                if not result:
                    self._cells[i][j].configure(foreground="red")
                    self._num_errors += 1
                    self._error_label.config(text=f"Errors: {self._num_errors}/{self.max_errors}")
                else:
                    self._cells[i][j].configure(foreground="black")
            except Exception as e:
                self._error_label.configure(text=str(e))
                self._gameover()
    
    def _gameover(self):
        for i in range(9):
            for j in range(9):
                self._cells[i][j].config(state="disabled")

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
