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
    def __init__(self, board, sign, train_count, epochs=10, data_in=27):
        DeepPlayer.__init__(self, board, sign, train_count)
        boards, values = self.load_data()
        self.X_train = boards
        self.Y_train = values
        self.epochs = epochs
        self.x_shape = data_in

        print(f'NN model having {train_count} training examples and {epochs} epochs with in-size {self.x_shape}')

    def load_data(self):
        with open('models/boards_' + str(self.training_count), 'rb') as f:
            board_data = pickle.load(f)
        with open('models/values_' + str(self.training_count), 'rb') as f:
            value_data = pickle.load(f)
        return board_data, value_data

    def filter_and_shuffle_data(self, init_value=0.2):
        board_data = self.X_train
        value_data = self.Y_train
        x_data, y_data = [], []

        for i in range(len(board_data)):
            if all(val == init_value for val in value_data[i]) \
                    or not all(val == -1 or val == init_value for val in value_data[i]):  # filter non visited boards
                x_data.append(board_data[i])
                y_data.append(value_data[i])

        random.shuffle(x_data)
        random.shuffle(y_data)
        self.X_train = x_data
        self.Y_train = y_data
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

    def split_data_27in_9out(self):
        for i, board in enumerate(self.X_train):
            self.X_train[i] = [1 if j == -1 else 0 for j in board] \
                        + [1 if j == 1 else 0 for j in board] \
                        + [1 if j == 0 else 0 for j in board]

    def split_data_18in_1out(self):
        x_splitted, y_splitted = [], []
        for i, board in enumerate(self.X_train):
            for j in range(len(self.Y_train[i])):
                if self.Y_train[i][j] > -1:
                    x_splitted.append(board + self.Y_train[i])
                    y_splitted.append(self.Y_train[i][j])
        self.X_train = x_splitted
        self.Y_train = y_splitted

    def train_model(self):
        # self.filter_and_shuffle_data()  # not working

        if self.x_shape == 18:
            self.split_data_18in_1out()
        if self.x_shape == 27:
            self.split_data_27in_9out()

        out_layer = 9 if self.x_shape != 18 else 1
        model = self.create_nn_with_one_layer(hidd_layer=100, out_layer=out_layer)
        trained_model = model.fit(np.array(self.X_train), np.array(self.Y_train), epochs=self.epochs, verbose=0)
        self.model = model

    def split_board(self, board):
        if self.x_shape == 27:
            new_board = [1 if j == -1 else 0 for j in board] \
                        + [1 if j == 1 else 0 for j in board] \
                        + [1 if j == 0 else 0 for j in board]
        # elif self.x_shape == 18:
        #     found, i = True, 0
        #     while found:
        #         if list(board) == self.X_train[i][:9]:
        #             found = False
        #         i = i+1
        #     new_board = self.X_train[i-1]
        else:
            new_board = board
        return np.array([new_board])

    def predict(self, board):
        board = self.split_board(board[0])

        prediction_values = self.model.predict(board)
        if type(prediction_values) is float:
            return [prediction_values]
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



