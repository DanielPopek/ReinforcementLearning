from board import Board
from game import Game
from player import CROSS, OH
from q_learnig import QLearning
from random_player import RandomPlayer


if __name__ == "__main__":
    board = Board()
    x = RandomPlayer(board, CROSS)
    o = RandomPlayer(board, OH)

    game = Game(board, x, o)
    game.playGame(True)

    q_test = QLearning()
    q_test.trainOnSingleGame(game, verbose=True)
