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

    def setBoard(self,board):
        self.board=board


class DeepPlayer(Player):
    def __init__(self, board, sign, train_count, epochs=100):
        Player.__init__(self, "x" if sign == CROSS else "o", board, sign)
        self.X_train = None
        self.Y_train = None
        self.model = None
        self.training_count = str(train_count)
        self.epochs = epochs

    def train_model(self):
        return NotImplementedError

    def predict(self, board):
        return NotImplementedError
