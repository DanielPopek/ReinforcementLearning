from nn_player import NNPlayer
from training_functions import *
from q_learning_player import QLearningPlayer
from deep_q_learning_player import DeepQLearningPlayer
from random_player import RandomPlayer

import tensorflow.python.util.deprecation as deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False


def get_player_type(player):
    return player.__class__


def print_winning_statistics(wins, deep_learning_player_type=''):
    print(f'\nWINNING STATISTICS ' + (f'for {deep_learning_player_type}' if deep_learning_player_type != ''
                                      else 'for QLearning'))
    print(f'X wins: {wins[2]}'
          f'\nO wins: {wins[0]}'
          f'\nDraws:  {wins[1]}')


''' Q learning '''


def single_qlearning_testing_game(q_test, x_qlearning=True, single_q_player=True, verbose=False):
    board = Board()
    if not x_qlearning and single_q_player:
        x = RandomPlayer(board, CROSS)
    else:
        x = QLearningPlayer(board, CROSS)

    if single_q_player and x_qlearning:
        o = RandomPlayer(board, OH)
    else:
        o = QLearningPlayer(board, OH)

    game = Game(board, x, o)
    game.play_game(verbose, q_test)

    # train qlearning table some more
    q_test.trainOnSingleGame(game, verbose=verbose)
    return game.board.getWinningSign()


def play_qlearning_train_and_test_games(train_count=3000):
    TRAIN_COUNT = train_count
    TEST_COUNT = 1000

    q_learning = QLearning()

    print('Training...')
    for i in range(TRAIN_COUNT):
        if i % 5000 == 4999:
            print('  ', i+1, 'iteration')
        single_qlearning_training_game(q_learning)

    # TEST
    print('\nTesting...')
    wins = [0, 0, 0]
    for i in range(TEST_COUNT):
        winner = single_qlearning_testing_game(q_learning, verbose=False, single_q_player=False)
        wins[winner + 1] += 1
    print_winning_statistics(wins)


''' Deep Q learning - sklearn and keras '''


def single_deep_qlearning_testing_game(player, x_deep_player=True, verbose=False):
    board = Board()

    if x_deep_player:
        x = player
        x.setBoard(board)
        o = RandomPlayer(board, OH)
    else:
        x = RandomPlayer(board, CROSS)
        o = player
        o.setBoard(board)

    game = Game(board, x, o)
    game.play_game(verbose)

    return game.board.getWinningSign()


def play_deep_qlearning_test_games(deep_learning_player_type='DeepQLearning', train_count=3000,
                                   is_deep_player_cross=True, verbose=True):
    TEST_COUNT = 1000

    if verbose:
        print('\nTraining...')
    board = Board()
    if deep_learning_player_type == 'DeepQLearning':
        player = DeepQLearningPlayer(board, CROSS if is_deep_player_cross else OH, train_count)
    if deep_learning_player_type == 'NN':
        player = NNPlayer(board, CROSS if is_deep_player_cross else OH, train_count)
    player.train_model()

    if verbose:
        print('Testing...')
    wins = [0, 0, 0]
    for i in range(TEST_COUNT):
        winner = single_deep_qlearning_testing_game(player, x_deep_player=is_deep_player_cross, verbose=False)
        wins[winner + 1] += 1

    if verbose:
        print_winning_statistics(wins, deep_learning_player_type)

    return wins


if __name__ == "__main__":
    play_qlearning_train_and_test_games()

    deep_learning_player_types = ['DeepQLearning', 'NN']
    play_deep_qlearning_test_games(deep_learning_player_type=deep_learning_player_types[0])
    play_deep_qlearning_test_games(deep_learning_player_type=deep_learning_player_types[1])

