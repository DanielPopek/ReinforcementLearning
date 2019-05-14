from nn_player import NNPlayer
from training_functions import *
from q_learning_player import QLearningPlayer
from deep_q_learning_player import DeepQLearningPlayer
from random_player import RandomPlayer

import tensorflow.python.util.deprecation as deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False

import pandas as pd
import seaborn as sns
sns.set()


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


def play_qlearning_train_and_test_games(train_count=3000,x_qlearning=True):
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
        winner = single_qlearning_testing_game(q_learning, x_qlearning=x_qlearning,verbose=False, single_q_player=False)
        wins[winner + 1] += 1
    print_winning_statistics(wins)
    return wins

def run_train_size_impact_test():
    TRAIN_COUNT = [200, 1000,  3000, 5000, 10000,15000,20000,25000]
    Q_X = [True,False]


    # need to change ending of file_name by hand
    file_name = f'Q_LEARNING_TRAIN_COUNT_IMPACT'

    df = pd.DataFrame(columns=['train_count','x_starts', 'x_wins', 'o_wins', 'draws'])
    print(df)

    for train_count in TRAIN_COUNT:
        for q_x in Q_X:
                wins = play_qlearning_train_and_test_games(train_count=train_count,x_qlearning=q_x)
                print(wins)
                df = df.append({ 'train_count': train_count,'x_starts':q_x,'x_wins': wins[2], 'o_wins': wins[0], 'draws': wins[1]}, ignore_index=True)

    df.to_csv('./csv_files/' + file_name + '.csv')
    return file_name




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
        player = NNPlayer(board, CROSS if is_deep_player_cross else OH, train_count, data_in=18, filter=True)
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
    #
    # play_train_games()
    # play_test_games_deep_player()
    # saveTrainingDataToFile()
    run_train_size_impact_test()
    # play_qlearning_train_and_test_games(train_count=30000)

    # deep_learning_player_types = ['DeepQLearning', 'NN']
    # # play_deep_qlearning_test_games(deep_learning_player_type=deep_learning_player_types[0])
    # play_deep_qlearning_test_games(deep_learning_player_type=deep_learning_player_types[1])
