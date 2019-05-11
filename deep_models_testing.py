from main import *
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set()

import tensorflow.python.util.deprecation as deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False


def single_deep_learning_run(deep_learning_player_type='DeepQLearning', train_count=3000,
                             is_deep_player_cross=True, epochs=100, data_shape=9, verbose=True):
    TEST_COUNT = 1000

    if verbose:
        print('\nTraining...')
    board = Board()
    if deep_learning_player_type == 'DeepQLearning':
        player = DeepQLearningPlayer(board, CROSS if is_deep_player_cross else OH, train_count, epochs)
    if deep_learning_player_type == 'NN':
        player = NNPlayer(board, CROSS if is_deep_player_cross else OH, train_count, epochs, data_in=data_shape)
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


def run_deep_learning_tests(deep_learning_player_type, verbose=True):
    TRAIN_COUNT = [5000]  # [100, 200, 500, 1000, 2000, 3000, 5000, 7500, 10000]
    epochs = [1, 2, 3, 5, 8, 10, 15, 20, 25]

    iterations = 10
    is_deep_player_x = False
    in_shape = 9

    file_name = f'{deep_learning_player_type}_in{in_shape}_iters{iterations}_isx{str(is_deep_player_x)}_' \
        f'lossAdam_optMSE_TC{TRAIN_COUNT[0]}_EPOCHS'

    df = pd.DataFrame(columns=['i', 'train_count', 'epochs', 'x_wins', 'o_wins', 'draws'])

    for train_count in TRAIN_COUNT:
        for iters in epochs:
            for i in range(iterations):
                wins = single_deep_learning_run(deep_learning_player_type=deep_learning_player_type,
                                                is_deep_player_cross=is_deep_player_x, train_count=train_count,
                                                epochs=iters, data_shape=in_shape, verbose=verbose)
                df = df.append({'i': i, 'train_count': train_count, 'epochs': iters,
                                'x_wins': wins[2], 'o_wins': wins[0], 'draws': wins[1]}, ignore_index=True)

    df.to_csv(file_name + '.csv')
    return file_name


def plot_model_results(file_name):
    data = pd.read_csv('C:/Users/Marta/Documents/Nauka/PyCharm/ReinforcementLearning/' + file_name + '.csv').iloc[:, 1:]
    fig, ax = plt.subplots()

    x = data.train_count.unique()
    x_wins, o_wins, draws = [], [], []

    for tc in list(x):
        filtered = data[data['train_count'] == tc]
        x_wins.append(filtered['x_wins'].mean())
        o_wins.append(filtered['o_wins'].mean())
        draws.append(filtered['draws'].mean())

    plt.plot(x, x_wins, label='X wins')
    plt.plot(x, o_wins, label='O wins')
    plt.plot(x, draws, label='Draws')

    #     plt.xlim(x[0], x[-1])
    plt.ylim((0, 1000))
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:,.0%}'.format(i / 1000) for i in vals])

    plt.legend(loc=7)
    plt.show()


if __name__ == '__main__':
    file_name = run_deep_learning_tests('NN')
    plot_model_results(file_name)


    # ''' Qlearning trainings saved to file '''
    # TRAIN_COUNT = [100, 200, 500, 1000, 2000, 3000, 5000, 7500, 10000]
    # for tc in TRAIN_COUNT:
    #     save_qlearning_training_data_to_file(tc)
