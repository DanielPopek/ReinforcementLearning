from board import Board
from game import Game
from player import CROSS, OH
from q_learnig import QLearning
from q_learning_player import QLearningPlayer
from deep_q_learning_player import DeepQLearningPlayer
from random_player import RandomPlayer

import ast
import pickle


def single_training_game(q_test, verbose=False):
    board = Board()
    x = RandomPlayer(board, CROSS)
    o = RandomPlayer(board, OH)
    game = Game(board, x, o)
    game.playGame(verbose=verbose)

    q_test.trainOnSingleGame(game, verbose=verbose)


def single_testing_game(q_test, single_q_player=True, verbose=False):
    board = Board()
    x = RandomPlayer(board, CROSS)
    if single_q_player:
        o = RandomPlayer(board, OH)
    else:
        o = QLearningPlayer(board, OH)

    game = Game(board, x, o)
    game.playGame(verbose, q_test)

    q_test.trainOnSingleGame(game, verbose=verbose)
    return game.board.getWinningSign()

def single_testing_game_deep_player( player, verbose=False):
    board = Board()
    x = RandomPlayer(board, CROSS)
    o = player
    o.setBoard(board)

    game = Game(board, x, o)
    game.playGame(verbose)

    return game.board.getWinningSign()


def play_test_games_deep_player():
    TEST_COUNT = 1000
    board = Board()
    q_learning_player = DeepQLearningPlayer(board, OH)
    q_learning_player.train_model()

    # TEST
    print('\nTesting...')
    wins = [0, 0, 0]
    for i in range(TEST_COUNT):
        winner = single_testing_game_deep_player(q_learning_player, verbose=False)
        wins[winner + 1] += 1

    print('\nWINNING STATISTICS FOR RANDOM')
    print(f'X wins: {wins[2]}\nO wins: {wins[0]}\nDraws:  {wins[1]}')




def play_train_games():
    TRAIN_COUNT = 100000
    TEST_COUNT = 1000

    q_learning = QLearning()

    print('Training...')
    for i in range(TRAIN_COUNT):
        if i % 5000 == 4999:
            print('  ', i+1, 'iteration')
        single_training_game(q_learning)

    # TEST
    print('\nTesting...')
    wins = [0, 0, 0]
    for i in range(TEST_COUNT):
        winner = single_testing_game(q_learning, verbose=False, single_q_player=False)
        wins[winner + 1] += 1

    print('\nWINNING STATISTICS FOR RANDOM')
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

def saveTrainingDataToFile():
    TRAIN_COUNT = 3000

    q_learning = QLearning()
    for i in range(TRAIN_COUNT):
        if i % 1000 == 999:
            print(i + 1, 'iteration')
        single_training_game(q_learning)

    boards, values = [], []
    for key, val in q_learning.state_action_dict.items():
        boards.append(ast.literal_eval(key))
        values.append(val)

    with open('boards_' + str(TRAIN_COUNT), 'wb') as f:
        pickle.dump(boards, f)
        print(boards)

    with open('values_' + str(TRAIN_COUNT), 'wb') as f:
        pickle.dump(values, f)
        print(values)


if __name__ == "__main__":
    play_train_games()
    play_test_games_deep_player()
    # saveTrainingDataToFile()

