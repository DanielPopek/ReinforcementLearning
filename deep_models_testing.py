from main import *
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set()

import tensorflow.python.util.deprecation as deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False


def single_deep_learning_run(deep_learning_player_type='DeepQLearning', train_count=3000,
                             is_deep_player_cross=True, epochs=100, data_shape=9, filter=False, verbose=True):
    TEST_COUNT = 1000

    if verbose:
        print('\nTraining...')
    board = Board()
    if deep_learning_player_type == 'DeepQLearning':
        player = DeepQLearningPlayer(board, CROSS if is_deep_player_cross else OH, train_count, epochs)
    if deep_learning_player_type == 'NN':
        player = NNPlayer(board, CROSS if is_deep_player_cross else OH, train_count, epochs,
                          data_in=data_shape, filter=filter)
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
    TRAIN_COUNT = [100, 200, 500, 1000, 2000, 3000, 5000, 7500, 10000]
    epochs = [10]  # [1, 2, 3, 5, 8, 10, 15, 20, 25]

    iterations = 10
    is_deep_player_x = False
    in_shape = 18
    filtering = True

    # need to change ending of file_name by hand
    file_name = f'{deep_learning_player_type}_in{in_shape}_iters{iterations}_isx{str(is_deep_player_x)}_' \
        f'lossAdam_optMSE{"_FILTERING" if filtering else ""}_epochs{epochs[0]}_TC'

    df = pd.DataFrame(columns=['i', 'train_count', 'epochs', 'x_wins', 'o_wins', 'draws'])

    for train_count in TRAIN_COUNT:
        for iters in epochs:
            for i in range(iterations):
                wins = single_deep_learning_run(deep_learning_player_type=deep_learning_player_type,
                                                is_deep_player_cross=is_deep_player_x, train_count=train_count,
                                                epochs=iters, data_shape=in_shape, filter=filtering, verbose=verbose)
                df = df.append({'i': i, 'train_count': train_count, 'epochs': iters,
                                'x_wins': wins[2], 'o_wins': wins[0], 'draws': wins[1]}, ignore_index=True)

    df.to_csv('./csv_files/' + file_name + '.csv')
    return file_name


def plot_model_results(file_name):
    data = pd.read_csv('./csv_files/' + file_name).iloc[:, 1:]
    fig, ax = plt.subplots()

    x_column_name = 'train_count'  # default
    if "EPOCHS.csv" in file_name:
        x_column_name = 'epochs'

    x = data[x_column_name].unique()
    x_wins, o_wins, draws = [], [], []
    colors = ['forestgreen', 'indianred', 'goldenrod']

    for val in list(x):
        filtered = data[data[x_column_name] == val]
        x_wins.append(filtered['x_wins'].mean())
        o_wins.append(filtered['o_wins'].mean())
        draws.append(filtered['draws'].mean())

    is_x = "isxTrue" in file_name
    plt.plot(x, x_wins, color=colors[0 if is_x else 1], label='X wins')
    plt.plot(x, o_wins, color=colors[1 if is_x else 0], label='O wins')
    plt.plot(x, draws, color=colors[2], label='Draws')

    #     plt.xlim(x[0], x[-1])
    plt.ylim((0, 1000))
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:,.0%}'.format(i / 1000) for i in vals])

    plt.xlabel(x_column_name)
    plt.ylabel('games won')

    plt.legend()
    plt.show()
    fig.savefig('./plots/' + file_name[:-4] + '_PLOT.png', dpi=150)


if __name__ == '__main__':
    # file_name = run_deep_learning_tests('NN')

    file_name = 'NN_in18_iters10_isxTrue_lossAdam_optMSE_epochs10_TC.csv'
    # # plotting (for now) only by train_count or epochs -> see implementation
    plot_model_results(file_name)


    # ''' Qlearning trainings saved to file '''
    # TRAIN_COUNT = [100, 200, 500, 1000, 2000, 3000, 5000, 7500, 10000]
    # for tc in TRAIN_COUNT:
    #     save_qlearning_training_data_to_file(tc)
