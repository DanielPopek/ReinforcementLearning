from player import *
import random


class RandomPlayer(Player):
    def __init__(self, board, sign):
        Player.__init__(self, "x" if sign == CROSS else "o", board, sign)

    def nextMove(self, qlearning=None, verbose=False):
        free_positions = self.board.getAllFreePositions()
        decision = random.choice(free_positions)
        if verbose:
            print(f'PLAYER: {self.name} on position {decision} - ({int(decision/3)}, {decision%3})')
        return decision
