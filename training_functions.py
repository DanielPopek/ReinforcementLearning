from board import Board
from game import Game
from player import OH, CROSS
from q_learnig import QLearning
from random_player import RandomPlayer

import ast
import pickle


def single_qlearning_training_game(q_test, verbose=False):
    board = Board()
    x = RandomPlayer(board, CROSS)
    o = RandomPlayer(board, OH)
    game = Game(board, x, o)
    game.play_game(verbose=verbose)

    q_test.trainOnSingleGame(game, verbose=verbose)


def save_qlearning_training_data_to_file():
    TRAIN_COUNT = 3000

    print('Training Qlearning...')
    q_learning = QLearning()
    for i in range(TRAIN_COUNT):
        if i % 1000 == 999:
            print('  ', i + 1, 'iteration')
        single_qlearning_training_game(q_learning)

    boards, values = [], []
    for key, val in q_learning.state_action_dict.items():
        boards.append(ast.literal_eval(key))
        values.append(val)

    with open('models/boards_' + str(TRAIN_COUNT), 'wb') as f:
        pickle.dump(boards, f)
        print(boards)

    with open('models/values_' + str(TRAIN_COUNT), 'wb') as f:
        pickle.dump(values, f)
        print(values)


def save_nn_trained_model_to_file(model, file_name):
    # serialize model to JSON
    model_json = model.to_json()
    with open('models/' + file_name + ".json", "w") as json_file:
        json_file.write(model_json)

    # serialize weights to HDF5
    model.save_weights('models/' + file_name + "_weights.h5")
    print("Saved model to disk")

