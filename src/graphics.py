from tkinter import Tk, Canvas

class Graphics:
    def __init__(self, width, height):
        self._root = Tk()
        self._root.title = "Sudoku"
        self._canvas = Canvas(self._root, background='white', width=width, height=height)
        self._canvas.pack()
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False
