from main import *
from plots import *

import pandas as pd
import seaborn as sns
sns.set()

import tensorflow.python.util.deprecation as deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False


def single_deep_learning_run(deep_learning_player_type='DeepQLearning', train_count=3000,
                             is_deep_player_cross=True, epochs=100, data_shape=9, filter=False, optimizer='adam', loss_type='mean_squared_error', hidden_size=100, hidden_layers=1, verbose=True):
    TEST_COUNT = 1000

    if verbose:
        print('\nTraining...')
    board = Board()
    if deep_learning_player_type == 'DeepQLearning':
        player = DeepQLearningPlayer(board, CROSS if is_deep_player_cross else OH, train_count, epochs)
    if deep_learning_player_type == 'NN':
        player = NNPlayer(board, CROSS if is_deep_player_cross else OH, train_count, epochs,
                          data_in=data_shape, filter=filter, optimizer=optimizer, loss_type=loss_type, hidden_size=hidden_size, hidden_layers=hidden_layers)
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
    # TRAIN_COUNT = [100, 200, 500, 1000, 2000, 3000, 5000, 7500, 10000]
    TRAIN_COUNT = [5000]
    epochs = [10]  # [1, 2, 3, 5, 8, 10, 15, 20, 25]

    iterations = 10
    is_deep_player_x = True
    in_shape = 9  # or 9 or 27
    filtering = False

    # need to change ending of file_name by hand
    file_name = f'{deep_learning_player_type}_in{in_shape}_iters{iterations}_isx{str(is_deep_player_x)}_' \
        f'lossAdam_optMSE{"_FILTERING" if filtering else ""}_epochs{epochs[0]}_TC2'

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


def loss_impact_test(deep_learning_player_type, verbose=True):
    LOSS_TYPES=['mean_squared_error','mean_absolute_error','mean_absolute_percentage_error','mean_squared_logarithmic_error','squared_hinge','hinge','categorical_hinge','logcosh']
    INPUT_SHAPES=[9,18,27]

    epochs = [10]  # [1, 2, 3, 5, 8, 10, 15, 20, 25]

    iterations = 10
    is_deep_player_x = True
    in_shape = 9  # or 9 or 27
    filtering = False

    # need to change ending of file_name by hand
    file_name = f'{deep_learning_player_type}_in{in_shape}_iters{iterations}_isx{str(is_deep_player_x)}_' \
        f'lossAdam_optMSE{"_FILTERING" if filtering else ""}_epochs{epochs[0]}_LOSS'

    df = pd.DataFrame(columns=['i', 'train_count', 'epochs', 'x_wins', 'o_wins', 'draws','loss','in_shape'])

    for loss in LOSS_TYPES:
        for input_shape in INPUT_SHAPES:
            for i in range(iterations):
                if(verbose):
                    print(f'LOSS {loss} - IN_SHAPE {input_shape}')
                wins = single_deep_learning_run(deep_learning_player_type=deep_learning_player_type,
                                                is_deep_player_cross=is_deep_player_x, train_count=5000,
                                                epochs=5, data_shape=input_shape, filter=filtering, optimizer='adam', loss_type=loss , hidden_size=100, hidden_layers=1, verbose=verbose)
                df = df.append({'i': i, 'train_count': 5000, 'epochs': 10,
                                'x_wins': wins[2], 'o_wins': wins[0], 'draws': wins[1],'loss':loss,'in_shape':input_shape}, ignore_index=True)

    df.to_csv('./csv_files/' + file_name + '.csv')
    return file_name

def optimizer_impact_test(deep_learning_player_type, verbose=True):
    LOSS_TYPES=['mean_squared_error','mean_absolute_error','mean_absolute_percentage_error','mean_squared_logarithmic_error','squared_hinge','hinge','categorical_hinge','logcosh']
    INPUT_SHAPES=[9,18,27]
    OPTIMIZERS=['adam','sgd','adadelta','adagrad']

    epochs = [10]  # [1, 2, 3, 5, 8, 10, 15, 20, 25]

    iterations = 10
    is_deep_player_x = True
    in_shape = 9  # or 9 or 27
    filtering = False

    # need to change ending of file_name by hand
    file_name = f'{deep_learning_player_type}_in{in_shape}_iters{iterations}_isx{str(is_deep_player_x)}_' \
        f'lossAdam_optMSE{"_FILTERING" if filtering else ""}_epochs{epochs[0]}_OPTIMIZER'

    df = pd.DataFrame(columns=['i', 'train_count', 'epochs', 'x_wins', 'o_wins', 'draws','optim','in_shape'])

    for optim in OPTIMIZERS:
            for i in range(iterations):
                if(verbose):
                    print(f'OPTIMIZER {optim}')
                wins = single_deep_learning_run(deep_learning_player_type=deep_learning_player_type,
                                                is_deep_player_cross=is_deep_player_x, train_count=5000,
                                                epochs=10, data_shape=in_shape, filter=filtering, optimizer=optim, loss_type='mean_squared_error' , hidden_size=100, hidden_layers=1, verbose=verbose)
                df = df.append({'i': i, 'train_count': 5000, 'epochs': 10,
                                'x_wins': wins[2], 'o_wins': wins[0], 'draws': wins[1],'optim':optim,'in_shape':in_shape}, ignore_index=True)

    df.to_csv('./csv_files/' + file_name + '.csv')
    return file_name

def hidden_size_impact_test(deep_learning_player_type, verbose=True):

    HIDDEN_SIZES=[10,20,40,50,100,150,200,300,500]

    epochs = [10]  # [1, 2, 3, 5, 8, 10, 15, 20, 25]

    iterations = 10
    is_deep_player_x = True
    in_shape = 9  # or 9 or 27
    filtering = False

    # need to change ending of file_name by hand
    file_name = f'{deep_learning_player_type}_in{in_shape}_iters{iterations}_isx{str(is_deep_player_x)}_' \
        f'lossAdam_optMSE{"_FILTERING" if filtering else ""}_epochs{epochs[0]}_HIDDEN_SIZE'

    df = pd.DataFrame(columns=['i', 'train_count', 'epochs', 'x_wins', 'o_wins', 'draws','hiden_size','in_shape'])

    for size in HIDDEN_SIZES:
            for i in range(iterations):
                if(verbose):
                    print(f'HIDDEN LAYER SIZE {size} ')
                wins = single_deep_learning_run(deep_learning_player_type=deep_learning_player_type,
                                                is_deep_player_cross=is_deep_player_x, train_count=5000,
                                                epochs=10, data_shape=in_shape, filter=filtering, optimizer='adam', loss_type='mean_squared_error' , hidden_size=size, hidden_layers=1, verbose=verbose)
                df = df.append({'i': i, 'train_count': 5000, 'epochs': 10,
                                'x_wins': wins[2], 'o_wins': wins[0], 'draws': wins[1],'hiden_size':size,'in_shape':in_shape}, ignore_index=True)

    df.to_csv('./csv_files/' + file_name + '.csv')
    return file_name

def hidden_size_impact_test_with_2_layers(deep_learning_player_type, verbose=True):

    HIDDEN_SIZES=[10,20,40,50,100,150,200,300,500]

    epochs = [10]  # [1, 2, 3, 5, 8, 10, 15, 20, 25]

    iterations = 5
    is_deep_player_x = True
    in_shape = 9  # or 9 or 27
    filtering = False

    # need to change ending of file_name by hand
    file_name = f'{deep_learning_player_type}_in{in_shape}_iters{iterations}_isx{str(is_deep_player_x)}_' \
        f'lossAdam_optMSE{"_FILTERING" if filtering else ""}_epochs{epochs[0]}_HIDDEN_SIZE_2_LAYERS'

    df = pd.DataFrame(columns=['i', 'train_count', 'epochs', 'x_wins', 'o_wins', 'draws','hiden_size','in_shape'])

    for size in HIDDEN_SIZES:
            for i in range(iterations):
                if(verbose):
                    print(f'HIDDEN LAYER SIZE {size} ')
                wins = single_deep_learning_run(deep_learning_player_type=deep_learning_player_type,
                                                is_deep_player_cross=is_deep_player_x, train_count=5000,
                                                epochs=10, data_shape=in_shape, filter=filtering, optimizer='adam', loss_type='mean_squared_error' , hidden_size=size, hidden_layers=2, verbose=verbose)
                df = df.append({'i': i, 'train_count': 5000, 'epochs': 10,
                                'x_wins': wins[2], 'o_wins': wins[0], 'draws': wins[1],'hiden_size':size,'in_shape':in_shape}, ignore_index=True)

    df.to_csv('./csv_files/' + file_name + '.csv')
    return file_name


def filter_impact_test(deep_learning_player_type, verbose=True):
    LOSS_TYPES=['mean_squared_error','mean_absolute_error','mean_absolute_percentage_error','mean_squared_logarithmic_error','squared_hinge','hinge','categorical_hinge','logcosh']
    INPUT_SHAPES=[9,18,27]
    FILTER=[True,False]
    epochs = [10]  # [1, 2, 3, 5, 8, 10, 15, 20, 25]

    iterations = 5
    is_deep_player_x = True
    in_shape = 9  # or 9 or 27
    filtering = False

    # need to change ending of file_name by hand
    file_name = f'{deep_learning_player_type}_in{in_shape}_iters{iterations}_isx{str(is_deep_player_x)}_' \
        f'lossAdam_optMSE{"_FILTERING" if filtering else ""}_epochs{epochs[0]}_FILTER'

    df = pd.DataFrame(columns=['i', 'train_count', 'epochs', 'x_wins', 'o_wins', 'draws','loss','filter','in_shape'])

    for input_shape in INPUT_SHAPES:
        for filter in FILTER:
            for i in range(iterations):
                if(verbose):
                    print(f'IN SHAPE {in_shape} - FILTER {filter}')
                wins = single_deep_learning_run(deep_learning_player_type=deep_learning_player_type,
                                                is_deep_player_cross=is_deep_player_x, train_count=5000,
                                                epochs=5, data_shape=input_shape, filter=filter, optimizer='adam', loss_type='mean_squared_error' , hidden_size=100, hidden_layers=1, verbose=verbose)
                df = df.append({'i': i, 'train_count': 5000, 'epochs': 10,
                                'x_wins': wins[2], 'o_wins': wins[0], 'draws': wins[1],'filter':filter,'in_shape':input_shape}, ignore_index=True)

    df.to_csv('./csv_files/' + file_name + '.csv')
    return file_name

def scheduled_test():
    # file_name = loss_impact_test('NN',verbose=False)
    file_name = optimizer_impact_test('NN', verbose=False)
    file_name = hidden_size_impact_test('NN', verbose=False)
    file_name = hidden_size_impact_test_with_2_layers('NN', verbose=False)
    file_name = filter_impact_test('NN', verbose=False)

if __name__ == '__main__':
    # file_name = run_deep_learning_tests('NN')
    file_name = loss_impact_test('NN')
    # ''' Qlearning trainings saved to file '''
    # TRAIN_COUNT = [100, 200, 500, 1000, 2000, 3000, 5000, 7500, 10000]
    # for tc in TRAIN_COUNT:
    #     save_qlearning_training_data_to_file(tc)
