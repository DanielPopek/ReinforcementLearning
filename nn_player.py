from player import *
import numpy as np


class NNPlayer(Player):
    def __init__(self, board, sign):
        Player.__init__(self, "x" if sign == CROSS else "o", board, sign)

    def nextMove(self, model, verbose=False):
        x = np.array(self.board.board).reshape(1, -1)
        pred = model.predict(x)[0]

        predictions = np.argsort(pred)[::-1]
        good_move, i = False, 0
        while not good_move:
            action = predictions[i]
            if self.board.board[action] == 0:
                good_move = True
            else:
                i = i + 1

        decision = action
        if verbose:
            print(f'Chosen move: {action}')

        if verbose:
            print(f'PLAYER: {self.name} on position {decision} - ({int(decision/3)}, {decision%3})')
        return decision
