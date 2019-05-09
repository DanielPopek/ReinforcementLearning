from player import *
import numpy as np


class QLearningPlayer(Player):
    def __init__(self, board, sign):
        Player.__init__(self, "x" if sign == CROSS else "o", board, sign)

    def next_move(self, qlearning, verbose=False):
        board = self.board.board
        if self.sign == OH:  # reverse values for OH sign player
            board = list(np.asarray(board) * -1)
        q_learning_values = qlearning.state_action_dict[str(board)]
        best_move = q_learning_values.index(max(q_learning_values))

        if verbose:
            print(f'Chosen move: {best_move} with Q table - {q_learning_values}')

        decision = best_move
        if verbose:
            print(f'PLAYER: {self.name} on position {decision} - ({int(decision/3)}, {decision%3})')
        return decision
