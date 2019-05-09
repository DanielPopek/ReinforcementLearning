from keras.engine.saving import model_from_json
from keras.initializers import glorot_uniform
from keras.utils import CustomObjectScope
import tensorflow as tf

from player import *
import numpy as np
import pickle
import random

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class NNPlayer(DeepPlayer):
    def __init__(self, board, sign, train_count, epochs=10):
        DeepPlayer.__init__(self, board, sign, train_count)
        boards, values = self.load_data()
        self.X_train = boards
        self.Y_train = values
        self.epochs = epochs

        print(f'NN model having {train_count} training examples and {epochs} epochs')

    def load_data(self):
        with open('models/boards_' + str(self.training_count), 'rb') as f:
            board_data = pickle.load(f)
        with open('models/values_' + str(self.training_count), 'rb') as f:
            value_data = pickle.load(f)
        return board_data, value_data

    def filter_and_shuffle_data(self, board_data, value_data, init_value=0.2):
        x_data, y_data = [], []

        for i in range(len(board_data)):
            if not all(val == -1 or val == init_value for val in value_data[i]):  # filter non visited boards
                x_data.append(board_data[i])
                y_data.append(value_data[i])

        random.shuffle(x_data)
        random.shuffle(y_data)
        return x_data, y_data

    def load_model_from_file(self, file_name):
        # load json and create model
        json_file = open('models/' + file_name + '.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
            loaded_model = model_from_json(loaded_model_json)

        # load weights into new model
        with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
            loaded_model.load_weights('models/' + file_name + "_weights.h5")
        print("Loaded model from disk")

        return loaded_model

    def create_nn_with_one_layer(self, hidd_layer, out_layer, optimizer='adam', loss='mean_squared_error'):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(hidd_layer, activation=tf.nn.relu),
            tf.keras.layers.Dense(out_layer, activation=tf.nn.softmax)
        ])
        model.compile(optimizer=optimizer, loss=loss)
        return model

    def train_model(self):
        model = self.create_nn_with_one_layer(hidd_layer=100, out_layer=9)
        trained_model = model.fit(np.array(self.X_train), np.array(self.Y_train), epochs=self.epochs, verbose=0)
        self.model = model

    def predict(self, board):
        prediction_values = self.model.predict(board)
        return prediction_values[0]

    def next_move(self, q_learning_table=None, verbose=False):
        board = self.board.board
        # if self.sign == OH:  # reverse values for OH sign player
        #     board = list(np.asarray(board) * -1)

        x = np.array(board).reshape(1, -1)
        pred = self.predict(x)

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



