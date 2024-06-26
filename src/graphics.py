from tkinter import Tk, Frame, StringVar, Entry, Label, Button, Radiobutton, IntVar, Checkbutton
import time


class GameWindow:
    def __init__(self, font_size=32):
        self._root = Tk()
        self._root.title("Sudoku")

        self._disable_game = False
        self._font_size = font_size
        self._running = False

        self._board = Frame(self._root, bg='white')
        self._board.grid(row=0, rowspan=9)
        self._build_game_frame()

        self._bottom_frame = Frame(self._root)
        self._bottom_frame.grid(row=10)
        self._build_bottom_frame()

        self._is_game_won = None
        self._play_func = None

        self._start_timer()
        self._root.protocol("WM_DELETE_WINDOW", self.close)

    """
    Public API functions:
    """

    def set_solve_callback(self, solve_func):
        self._solve_button.configure(
            command=lambda: [self.disable_game(), self._start_timer(), solve_func(), self._handle_autosolve_complete()])

    def set_view_solution_callback(self, callback):
        self._view_solution_button.config(command=callback)

    def set_max_errors(self, max_errors):
        self._max_errors = max_errors
        self.info_label.configure(
            text=f"Errors: {self._num_errors}/{self._max_errors}")

    def set_max_hints(self, max_hints):
        self._max_hints = max_hints
        self._hint_label.config(
            text=f"Hints {self._num_hints}/{self._max_hints}")

    def set_hint_callback(self, hint_func):
        self._get_hint = hint_func

    def set_play_callback(self, play_func):
        self._play_func = play_func

    def disable_game(self):
        self._disable_game = True

    def set_win_condition(self, win):
        self._is_game_won = win

    def draw(self, board):
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

    """
    Private helper functions:
    """

    def _start_timer(self):
        self._start_time = time.time()

    def _build_cells(self):
        frames = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                frames[i][j] = Frame(
                    self._board, bd=1, highlightbackground='black', highlightthickness=1)
                frames[i][j].grid(row=i, column=j, sticky='nsew')

        self._cells = [[None]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                cell = Frame(frames[i//3][j//3])
                cell.grid(row=i % 3, column=j % 3, sticky='nsew')
                self._contents[i][j] = StringVar(name=f'{i},{j}')
                self._cells[i][j] = Entry(cell, bg='white', width=3, textvariable=self._contents[i][j],
                                          justify='center', foreground='black', font=(f"Arial {self._font_size}"))
                self._cells[i][j].grid(sticky='nsew')

                self._contents[i][j].trace_add("write", self._handle)

    def _update_hints(self, cell):
        hint = self._get_hint(cell)
        if hint is not None:
            self.update_cell(*cell, hint, False)
            self._num_hints += 1
            self._hint_label.config(
                text=f"Hints {self._num_hints}/{self._max_hints}")
            return True
        return False

    def _handle(self, name, handle, op):
        if self._disable_game or self._play_func is None:
            return

        indices = name.split(',')
        i, j = int(indices[0]), int(indices[1])
        contents_str = self._contents[i][j].get().strip()

        # Handle the case where the user is asking for a hint
        if '?' in contents_str:
            result = self._update_hints((i, j))
            if result:
                return

        # Verify that the entry is valid
        if contents_str.isnumeric():
            contents = int(contents_str)
        else:
            self._cells[i][j].configure(foreground="red")
            return

        # If it is, make the play, and update the board with the result.
        args = (i, j, contents)
        try:
            result = self._play_func(args)
            if not result:
                self._cells[i][j].configure(foreground="red")
                self._num_errors += 1
                self.info_label.config(
                    text=f"Errors: {self._num_errors}/{self._max_errors}")
            else:
                self._cells[i][j].configure(foreground="black")
                self._handle_win()

        except Exception as e:
            self.info_label.configure(text=str(e))
            self._gameover()

    def _handle_autosolve_complete(self):
        done = self._is_game_won()
        if done:
            self.info_label.config(
                text=f"Solver completed in {int(time.time() - self._start_time)} seconds")
        self._hint_label.destroy()
        self._view_solution_button.invoke()

    def _handle_win(self):
        gamewon = self._is_game_won()
        if gamewon:
            self.info_label.config(
                text=f"Congratulations! You won! time elapsed: {int(time.time() - self._start_time)} seconds")

    def _gameover(self):
        for i in range(9):
            for j in range(9):
                self._cells[i][j].config(state="disabled")
        self._hint_label.destroy()

    def _build_game_frame(self):
        self._contents = [[None]*9 for _ in range(9)]
        self._cells = [[None]*9 for _ in range(9)]
        self._build_cells()

    def _build_bottom_frame(self):
        self.info_label = Label(self._bottom_frame)
        self.info_label.grid(row=0, column=1)
        self._num_errors = 0
        self._num_hints = 0
        self._max_errors = 3
        self._max_hints = 3

        self._hint_label = Label(self._bottom_frame)
        self._hint_label.grid(row=0, column=4)
        self._solve_button = Button(self._bottom_frame, text="Solve")
        self._solve_button.grid(row=0, column=0)

        self._view_solution_button = Button(
            self._bottom_frame, text="View Solution")
        self._view_solution_button.grid(row=0, column=3)


class MenuWindow:
    def __init__(self):
        self._root = Tk()
        self._root.title("Sudoku Solver")
        self._root.grid()

        self._solver_frame = Frame(self._root, relief='solid', borderwidth=1)
        self._solver_frame.grid(row=0, column=1, padx=5)
        self._solver_selection = StringVar(self._root, "1")
        self._build_solver_selector()

        self._difficulty_frame = Frame(self._root, relief='solid', borderwidth=1)
        self._difficulty_frame.grid(row=0, column=0)
        self._difficulty_selection = StringVar(self._root, "45")

        self._bottom_frame = Frame(self._root, relief='solid', borderwidth=1)
        self._bottom_frame.grid(row=1, column=0, columnspan=2, padx=2, pady=5)
        
        self._build_difficulty_selector()

        self._build_errors_allowed()
        self._build_hints_allowed()
        self._build_autosolve_config()

        self._start = False

        self._start_button = Button(
            self._bottom_frame, text="Start Game!", command=lambda: [self._set_start(), self._root.destroy()])
        self._start_button.grid(row=5, column=1)

    def start(self):
        self._root.mainloop()
        return self._build_configuration()

    def _set_start(self):
        self._start = True

    def _build_configuration(self):
        num_hints = int(self._num_hints.get())
        num_errors = int(self._num_errors.get())
        timer = float(self._timer.get())
        visualize = bool(self._do_autosolve.get())
        solver_selection = int(self._solver_selection.get())
        difficulty_selection = int(self._difficulty_selection.get())
        config = {
            'start': self._start,
            'num_hints': num_hints,
            'num_errors': num_errors,
            'timer': timer,
            'visualize': visualize,
            'solver_type': solver_selection,
            'difficulty': difficulty_selection
        }
        return config

    def _build_solver_selector(self):
        options = {
            'Default Solver': '1',
            'AC-3 Solver': '2',
            'MRV Heuristic': '3',
            'Forward Checking': '4'
        }
        label = Label(self._solver_frame, text="Solver Algorithm").pack(side="top")
        for (key, value) in options.items():
            Radiobutton(self._solver_frame, text=key, value=value,
                        variable=self._solver_selection).pack(side="top", ipady=5)

    def _build_difficulty_selector(self):
        options = {
            'Easy': '55',
            'Medium': '45',
            'Hard': '35',
            'Very Hard': '30',
        }
        label = Label(self._difficulty_frame, text="Puzzle difficulty").pack(side="top")
        for (key, value) in options.items():
            Radiobutton(self._difficulty_frame, text=key, value=value,
                        variable=self._difficulty_selection).pack(side="top", ipady=5)

    def _build_errors_allowed(self):
        self._num_errors = StringVar(self._bottom_frame, '3')
        error_label = Label(self._bottom_frame, text="Errors allowed: ")
        error_label.grid(row=1, column=0)
        self._num_errors_entry = Entry(
            self._bottom_frame, textvariable=self._num_errors, width=5)
        self._num_errors_entry.grid(row=1, column=1)

    def _build_hints_allowed(self):
        self._num_hints = StringVar(self._bottom_frame, '3')
        hint_label = Label(self._bottom_frame, text="Hints allowed: ")
        hint_label.grid(row=2, column=0)
        self._num_hints_entry = Entry(
            self._bottom_frame, textvariable=self._num_hints, width=5)
        self._num_hints_entry.grid(row=2, column=1)

    def _build_autosolve_config(self):
        self._timer = StringVar(self._bottom_frame, '0.05')
        timer_label = Label(self._bottom_frame, text="Autosolve delay: ")
        timer_label.grid(row=3, column=0)
        self._timer_entry = Entry(
            self._bottom_frame, textvariable=self._timer, width=5
        )
        self._timer_entry.grid(row=3, column=1)

        self._do_autosolve = IntVar(self._bottom_frame, 1)
        autosolve_label = Label(self._bottom_frame, text="Visualize Autosolver?")
        autosolve_label.grid(row=4, column=0)
        self._do_autosolve_box = Checkbutton(
            self._bottom_frame, variable=self._do_autosolve, onvalue=1, offvalue=0)
        self._do_autosolve_box.grid(row=4, column=1)
