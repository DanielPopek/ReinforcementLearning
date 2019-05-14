import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set()


def plot_single_model_results_linear(file_name):
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


def plot_single_model_result_pie(file_name, param_value=5000):
    labels = 'X', 'O', 'Draw'
    data = pd.read_csv('./csv_files/' + file_name).iloc[:, 1:]
    fig, ax = plt.subplots()

    x_column_name = 'train_count'  # default
    if "EPOCHS.csv" in file_name:
        x_column_name = 'epochs'

    is_x = "isxTrue" in file_name
    x = data[x_column_name].unique()
    colors = ['forestgreen' if is_x else 'indianred', 'indianred' if is_x else 'forestgreen', 'goldenrod']

    sizes = []
    filtered = data[data[x_column_name] == param_value]
    sizes.append(filtered['x_wins'].mean())
    sizes.append(filtered['o_wins'].mean())
    sizes.append(filtered['draws'].mean())

    explode = (0.1, 0, 0) if is_x else (0, 0.1, 0)

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.show()
    fig.savefig('./plots/' + file_name[:-4] + '_' + str(param_value) + '_PIE_CHART.png', dpi=150)


if __name__ == '__main__':
    file_name = 'NN_in9_iters10_isxTrue_lossAdam_optMSE_epochs10_TC.csv'
    # file_name='NN_in18_iters10_isxFalse_lossAdam_optMSE_FILTERING_epochs10_TC2.csv'
    plot_single_model_result_pie(file_name,param_value=100)
    plot_single_model_results_linear(file_name)
