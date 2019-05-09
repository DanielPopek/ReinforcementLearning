from board import Board
from player import UNKNOWN, CROSS, OH
from random_player import RandomPlayer

import numpy as np


class Game(object):

    # Historia ma postać
    # history=[(stateHash,action),(stateHash,action)..] np. [(233dsw2,2),(232345,1),...]
    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.playerActive = player1
        self.playerInactive = player2
        self.player1History = []
        self.player2History = []

    def switchPlayers(self):
        if self.playerActive == self.player1:
            self.playerActive = self.player2
            self.playerInactive = self.player1
        else:
            self.playerActive = self.player1
            self.playerInactive = self.player2

    def putHistoryTuple(self, player, board, action):
        sign = player.sign
        history = self.player1History if player == self.player1 else self.player2History
        # hash = None
        if sign == CROSS:
            hash = board.getHash()
        else:
            hash = board.getRevertHash()
        history.append((hash, action))

    def play_game(self, verbose, q_learning_table=None):
        move = 0
        winner = UNKNOWN
        while winner == UNKNOWN and not self.board.isFull():
            action = self.playerActive.next_move(q_learning_table, verbose)
            self.putHistoryTuple(self.playerActive, self.board, action)
            self.board.board[action] = self.playerActive.sign
            self.switchPlayers()
            winner = self.board.getWinningSign()
            move += 1
        if verbose:
            self.board.printBoardFormatted()
            # self.board.printBoard()
            if self.board.getWinningSign() != UNKNOWN:
                sign = self.board.getWinningSign()
                print(f'\nTHE WINNER IS: PLAYER {self.get_winner(sign).name}\n')
            else:
                print('\nDRAW :)\n')
            print(f'Player 1: {self.player1History}')
            print(f'Player 2: {self.player2History}')

    def get_winner(self, sign):
        if self.player1.sign == sign:
            return self.player1
        else:
            return self.player2
