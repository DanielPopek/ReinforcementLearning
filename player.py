CROSS = 1
OH = -1
UNKNOWN = 0


class Player(object):
    def __init__(self, name, board, sign):
        self.name = name
        self.board = board
        self.sign = sign

    def next_move(self, qlearning=None, verbose=False):
        return NotImplementedError
