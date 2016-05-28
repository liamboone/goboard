from collections import defaultdict

class Board:
    neighbors = ((-1, 0), (0, -1), (1, 0), (0, 1))

    def __init__(self, dim):
        self.dim = dim
        self.last_move = None
        self.board = defaultdict(int)
        self.captured = defaultdict(int)

    def _in_bounds(self, row, col):
        return row >= 0 and row < self.dim and col >= 0 and col < self.dim

    def _find_group(self, row, col, stones=None):
        if stones is None:
            stones = {(row, col)}

        for r, c in self.neighbors:
            r += row
            c += col
            if (r, c) not in stones and self._in_bounds(r, c):
                if self.board[r, c] == self.board[row, col]:
                    stones.add((r, c))
                    self._find_group(r, c, stones)

        return stones

    def _find_liberties(self, stones):
        liberties = set()
        for row, col in stones:
            for r, c in self.neighbors:
                r += row
                c += col
                if self._in_bounds(r, c):
                    liberties.add(self.board[r, c])

        return 0 in liberties

    def play_move(self, player, row, col):
        if self.board[row, col] != 0:
            print "*** Space not empty"
            return

        self.board[row, col] = player
        self.last_move = (row, col)

        for r, c in self.neighbors + ((0, 0),):
            r += row
            c += col
            if self._in_bounds(r, c):
                stones = self._find_group(r, c)

                if not self._find_liberties(stones):
                    self.captured[player] += len(stones)
                    for stone in stones:
                        self.board[stone] = 0

    def get_player_stones(self, player):
        return {coord for coord, color in self.board.iteritems() if color == player}

    def get_player_captures(self, player):
        return self.captured[player]

    def print_board(self):
        print
        for r in range(self.dim):
            row_str = ""
            for c in range(self.dim):
                if (r, c) == self.last_move:
                    row_str += "("
                elif (r, c-1) == self.last_move:
                    row_str += ""
                else:
                    row_str += " "

                row_str += {0: ".", 1: "X", 2: "O"}[self.board[r, c]]

                if (r, c) == self.last_move:
                    row_str += ")"
            print row_str
        print
