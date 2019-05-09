from main import *

import tensorflow.python.util.deprecation as deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False


def single_deep_learning_run(deep_learning_player_type='DeepQLearning', train_count=3000, verbose=True):
    TEST_COUNT = 1000
    is_deep_player_cross = True

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


def run_single_test(deep_learning_player_type, verbose=True):
    wins = play_deep_qlearning_test_games(deep_learning_player_type=deep_learning_player_type)



if __name__ == '__main__':
    pass