from board import Board
from game import Game
from player import CROSS, OH
from q_learnig import QLearning
from q_learning_player import QLearningPlayer
from random_player import RandomPlayer


def single_training_game(q_test, verbose=False):
    board = Board()
    x = RandomPlayer(board, CROSS)
    o = RandomPlayer(board, OH)
    game = Game(board, x, o)
    game.playGame(verbose=verbose)

    q_test.trainOnSingleGame(game, verbose=verbose)


def single_testing_game(q_test, single_q_player=True, verbose=False):
    board = Board()
    x = QLearningPlayer(board, CROSS)
    if single_q_player:
        o = RandomPlayer(board, OH)
    else:
        o = QLearningPlayer(board, OH)

    game = Game(board, x, o)
    game.playGame(verbose, q_test)
    return game.board.getWinningSign()


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
        winner = single_testing_game(q_learning, verbose=False, single_q_player=True)
        wins[winner + 1] += 1

    print('\nWINNING STATISTICS')
    print(f'X wins: {wins[2]}\nO wins: {wins[0]}\nDraws:  {wins[1]}')

    # for i in range(TEST_COUNT):
    #     board = Board()
    #     x = RandomPlayer(board, CROSS)
    #     o = QLearning(board, OH)
    #     game = Game(board, x, o)
    #     game.playGame(True)


if __name__ == "__main__":
    play_train_games()


    # board = Board()
    # x = RandomPlayer(board, CROSS)
    # o = RandomPlayer(board, OH)
    #
    # game = Game(board, x, o)
    # game.playGame(True)
    #
    # q_test = QLearning()
    # q_test.trainOnSingleGame(game, verbose=True)

