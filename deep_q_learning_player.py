import numpy as np
import pickle
from player import *
import numpy as np
from sklearn.neural_network import MLPRegressor
from matplotlib import pyplot as plt

# FILE_NAME_SUFFIX = '3000'


class DeepQLearningPlayer(DeepPlayer):
    # -1 ==oh, 1== cross, 0== undefined
    def __init__(self, board, sign, train_count, epochs=1000):
        DeepPlayer.__init__(self, board, sign, train_count)
        self.X_train = self.load_boards_from_file()[0]
        self.Y_train = self.load_values_from_file()[0]
        self.epochs = epochs

    def load_boards_from_file(self):
        boards = []
        with (open("models/boards_" + self.training_count, "rb")) as openfile:
            while True:
                try:
                    boards.append(pickle.load(openfile))
                except EOFError:
                    break
        return boards

    def load_values_from_file(self):
        values = []
        with (open("models/values_" + self.training_count, "rb")) as openfile:
            while True:
                try:
                    values.append(pickle.load(openfile))
                except EOFError:
                    break
        return values

    def train_model(self):
        model = MLPRegressor(max_iter=self.epochs)
        model.fit(X=self.X_train, y=self.Y_train)
        self.model = model

    def predict(self, board):
        prediction_values = self.model.predict(board)
        return prediction_values

    def next_move(self, qlearning=None, verbose=False):
        board = self.board.board
        # if self.sign == OH:  # reverse values for OH sign player
        #     board = list(np.asarray(board) * -1)

        q_learning_values = self.model.predict([board])[0].tolist()
        best_move = q_learning_values.index(max(q_learning_values))

        if verbose:
            print(f'Chosen move: {best_move} with Q table - {q_learning_values}')

        decision = best_move
        if verbose:
            print(f'PLAYER: {self.name} on position {decision} - ({int(decision / 3)}, {decision % 3})')
        return decision

