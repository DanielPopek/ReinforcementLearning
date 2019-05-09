from itertools import product
from board import Board
from random_player import *
from game import Game
import numpy as np


WIN_VALUE = 1
LOS_VALUE = 0


class QLearning(object):
    # assumes that the state-action matrix is a dictionary <stateHash:string, actionsQ:real>
    # actions are in order row by row : [top-lef,top-middle,top-right,middle-left....,down-right]
    # states are perceived from the perspective of CROSSes (sign 1)
    # in order to update state's Qs for Os, the board hash has to be previously inverted --> in Game class

    ALPHA = 0.7
    GAMMA = 0.95
    INITIALIZING_VALUE = 0.2  # 1 - optimistic, 0 - pessimistic, 0.5 normal (draw)

    def __init__(self):
        self.state_action_dict = self.generateStatesActionsDict()

    def generateAllStates(self):
        allStates = list(product([-1, 0, 1], repeat=9))
        allStatesLists = [list(i) for i in allStates]
        return allStatesLists

    def generateStatesActionsDict(self):
        allStatesLists = self.generateAllStates()
        statesActionsDict = {}
        for l in allStatesLists:
            q_values = [self.INITIALIZING_VALUE if i == UNKNOWN else -1 for i in l]
            statesActionsDict[str(l)] = q_values
        return statesActionsDict

    def update_Qvalue_for_state_from(self, stateFrom_action_stateTo, verbose=False):
        state_from, action, state_to = stateFrom_action_stateTo
        q_values_from = self.state_action_dict[state_from]
        q_values_to = self.state_action_dict[state_to]
        max_value = np.max(q_values_to)

        new_q_value = (1 - self.ALPHA) * q_values_from[action] + self.ALPHA * self.GAMMA * max_value
        q_values_from[action] = new_q_value
        if verbose:
            print(q_values_from)

    def trainOnSingleGame(self, game, verbose=False):
        winner_sign = game.board.getWinningSign()
        p1_hist, p2_hist = game.player1History[::-1], game.player2History[::-1]

        if verbose:
            print('\nPlayer 1:')
        self.update_Qlearning_based_on_player_history(p1_hist, winner_sign, verbose=verbose)

        if verbose:
            print('\nPlayer 2:')
        # p2_hist = self.reverse_history(p2_hist)
        self.update_Qlearning_based_on_player_history(p2_hist, -winner_sign, verbose=verbose)
        # for state, action in p1_hist:
        #     # TODO implement
        #     print('\nState and action:', state, action)
        #     # self.updateStateQValues(str(state))
        #
        # # for state, action in p2_hist:
        # #     # TODO implement
        # #     print(state, action)

    # def reverse_history(self, player_hist):
    #     p2_reversed_hist = []
    #     for history in player_hist:
    #         new_state = history[0].split(',')
    #         new_state[0] = new_state[0][1:]
    #         new_state[-1] = new_state[-1][:-1]
    #         for i in range(len(new_state)):
    #             new_state[i] = int(new_state[i]) * -1
    #         p2_reversed_hist.append([str(new_state), history[1]])
    #
    #     return p2_reversed_hist

    def update_Qlearning_based_on_player_history(self, player_history, winning_prize, verbose=False):
        last_move_state, last_move_action = player_history[0]
        self.state_action_dict[str(last_move_state)][last_move_action] = (winning_prize + 1) / 2
        if verbose:
            print(self.state_action_dict[str(last_move_state)])

        # generating history of moves - for easier Q learning values update
        state_action_state_list = []
        for i in range(len(player_history) - 1):
            state_action_state_list.append([str(player_history[i + 1][0]), player_history[i + 1][1], str(player_history[i][0])])
            self.update_Qvalue_for_state_from(state_action_state_list[i], verbose=verbose)
            # print(i, '-', state_action_state_list[i])


    def trainRandomPlayers(self, gamesCount):
        for i in range(gamesCount):
            board = Board()
            player1 = RandomPlayer(board, OH)
            player2 = RandomPlayer(board, CROSS)
            game = Game(board, player1, player2)
            self.trainOnSingleGame(game)


