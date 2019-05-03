from keras.engine.saving import model_from_json
from keras.initializers import glorot_uniform
from keras.utils import CustomObjectScope

from board import Board
from game import Game
from main_qlearning import play_train_games
from nn_player import NNPlayer
from player import CROSS, OH
from q_learnig import QLearning
from q_learning_player import QLearningPlayer
from random_player import RandomPlayer

import ast
import pickle


def single_testing_game(model, single_q_player=True, verbose=False):
    board = Board()
    x = NNPlayer(board, CROSS)
    if single_q_player:
        o = RandomPlayer(board, OH)
    else:
        o = NNPlayer(board, OH)

    game = Game(board, x, o)
    game.play_game(verbose, model)

    return game.board.getWinningSign()


def play_games_with_trained_model(model, test_games=1000):
    TEST_COUNT = test_games

    wins = [0, 0, 0]
    for i in range(TEST_COUNT):
        winner = single_testing_game(model, verbose=False, single_q_player=True)
        wins[winner + 1] += 1

    print('\nWINNING STATISTICS')
    print(f'X wins: {wins[2]}\nO wins: {wins[0]}\nDraws:  {wins[1]}')

    # wins = [0, 0, 0]
    # for i in range(TEST_COUNT):
    #     winner = single_testing_game(q_learning, verbose=False, single_q_player=False)
    #     wins[winner + 1] += 1
    #
    # print('\nWINNING STATISTICS FOR BOTH Q LEARNING PLAYERS')
    # print(f'X wins: {wins[2]}\nO wins: {wins[0]}\nDraws:  {wins[1]}')


    # for i in range(TEST_COUNT):
    #     board = Board()
    #     x = RandomPlayer(board, CROSS)
    #     o = QLearning(board, OH)
    #     game = Game(board, x, o)
    #     game.playGame(True)


def load_model_from_file(file_name):
    # load json and create model
    json_file = open(file_name + '.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        loaded_model.load_weights(file_name + "_weights.h5")
    print("Loaded model from disk")

    return loaded_model


if __name__ == "__main__":
    model = load_model_from_file("test_model_500000")
    play_games_with_trained_model(model)

    # play_train_games()




