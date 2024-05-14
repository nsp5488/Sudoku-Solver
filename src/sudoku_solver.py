import time
from collections import deque
import heapq

class SudokuSolver:
    def __init__(self, generating_board=False, visualize=False, visualize_timer=0.05, use_ac3=True, 
                 use_mrv=True, use_forward_checking=True):
        self._generating_board = generating_board
        self._num_solutions = 0
        self._board = []
        self._visualize = visualize
        self._vis_update = None
        self._visualize_timer = visualize_timer
        self._use_ac3 = use_ac3
        self._use_mrv = use_mrv
        self._use_forward_checking = use_forward_checking

    def _lock_board_by_domains(self):
        for i in range(9):
            for j in range(9):
                if len(self._domains[i][j]) == 1:
                    self._board[i][j] = list(self._domains[i][j])[0]
                    if self._visualize:
                        self._vis_update((i, j, self._board[i][j], False))

    def solve(self, board, row, col):
        self._board = board
        if self._use_ac3:
            self._domains = self._build_domains(board)
            arcs = self._build_arcs()
            solvable = self._ac3(arcs)

            # We can only take advantage of this optimization if we're not generating a board.
            if not self._generating_board:
                self._lock_board_by_domains()

            
            if not solvable:
                return False

            if self._use_mrv:
                self._mrv_heap = self._build_mrv_heap()
                return self._mrv_backtrack()
            
        # Default backtracker 
        return self._fill_board(row, col)

    def get_solved_board(self):
        return self._board

    def set_visualize_display(self, vis_update):
        self._vis_update = vis_update

    def constraint_propogation(self):
        pass

    def _forward_check(self, xi, value):
        removed = []
        for neighbor in self._get_neighbors(xi):
            if value in self._domains[neighbor[0]][neighbor[1]]:
                if len(self._domains[neighbor[0]][neighbor[1]]) == 1:
                    return (False, removed)
                else:
                    self._domains[neighbor[0]][neighbor[1]].remove(value)
                    removed.append(neighbor)
        return (True, removed)
    
    def _undo_forward_check(self, value, removed):
        for neighbor in removed:
            self._domains[neighbor[0]][neighbor[1]].add(value)

    def _build_mrv_heap(self):
        # flatten the domain array:
        heap = []
        self._n_remaining = 81
        for i in range(9):
            for j in range(9):
                if len(self._domains[i][j]) == 1:
                    self._n_remaining -= 1
                else:
                    heapq.heappush(heap, (len(self._domains[i][j]), (i, j)))

        return heap

    def _build_domains(self, board):
        domains = [[None]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    domains[i][j] = set(e for e in range(1, 10))
                else:
                    domains[i][j] = set()
                    domains[i][j].add(board[i][j])
        return domains

    def _build_arcs(self):
        arcs = []
        for i in range(9):
            for j in range(9):
                for neighbor in self._get_neighbors((i, j)):
                    arcs.append(((i, j), neighbor))
        return arcs

    def _get_neighbors(self, cell):
        i, j = cell
        cell_row = i - i % 3
        cell_col = j - j % 3
        neighbors = []
        for x in range(9):
            if (x, j) != cell:
                neighbors.append((x, j))
            if (i, x) != cell:
                neighbors.append((i, x))

        for x in range(cell_row, cell_row + 3):
            for y in range(cell_col, cell_col + 3):
                if (x, y) != cell and (x, y) not in neighbors:
                    neighbors.append((x, y))
        return neighbors

    def _revise(self, xi, xj):
        revised = False
        removing = set()
        for value in self._domains[xi[0]][xi[1]]:
            if value in self._domains[xj[0]][xj[1]] and len(self._domains[xj[0]][xj[1]]) == 1:
                revised = True
                removing.add(value)
        self._domains[xi[0]][xi[1]] -= removing
        return revised

    def _ac3(self, arcs):
        queue = deque()
        for arc in arcs:
            queue.append(arc)
        while len(queue) > 0:
            (xi, xj) = queue.popleft()
            if self._revise(xi, xj):
                if len(self._domains[xi[0]][xi[1]]) == 0:
                    return False
                for neighbor in self._get_neighbors(xi):
                    if neighbor == xj:
                        continue
                    queue.append((xi, neighbor))
        return True

    def _mrv_backtrack(self):
        if self._generating_board and self._num_solutions > 1:
            return False
        if self._n_remaining == 0:
            self._num_solutions += 1
            return not self._generating_board
        
        if len(self._mrv_heap) > 0:
            row, col = heapq.heappop(self._mrv_heap)[1] # index 0 contains priority, index 1 is a tuple of row, col
            while self._board[row][col] > 0 and len(self._mrv_heap) > 0:
                row, col = heapq.heappop(self._mrv_heap)[1]
        else:
            return False
        
        for value in self._get_domain(row, col):
            if self._use_forward_checking:
                result, removed = self._forward_check((row,col), value)
                if not result:
                    self._undo_forward_check(value, removed)
                    continue

            if self._visualize:
                self._vis_update((row, col, value, not check_play(self._board, row, col, value)))
                time.sleep(self._visualize_timer)

            if check_play(self._board, row, col, value):
                self._board[row][col] = value
                self._n_remaining -= 1
                if self._mrv_backtrack():
                    return True
            if self._use_forward_checking:
                self._undo_forward_check(value, removed)
        if self._visualize:
            self._vis_update((row, col, 0))

        self._board[row][col] = 0
        heapq.heappush(self._mrv_heap, (len(self._domains[row][col]), (row, col)))
        self._n_remaining += 1
        return False

    def _get_domain(self, row, col):
        if self._use_ac3:
            return list(self._domains[row][col])
        else:
            return range(1, 10)

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
        for value in self._get_domain(row, col):
            if self._visualize:
                self._vis_update(
                    (row, col, value, not check_play(self._board, row, col, value)))
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
    cell_row = i - i % 3  # These represent the top left coordinate of the cell
    cell_col = j - j % 3
    for x in range(cell_row, cell_row + 3):
        for y in range(cell_col, cell_col + 3):
            if board[x][y] == value:
                return False

    return True
