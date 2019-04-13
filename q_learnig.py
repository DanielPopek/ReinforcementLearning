from itertools import product
from board import Board
from random_player import RandomPlayer
from game import Game
import numpy as np
class QLearning(object):
    #assumes that the state-action matrix is a dictionary <stateHash:string, actionsQ:real>
    #actions are in order row by row : [top-lef,top-middle,top-right,middle-left....,down-right]
    #states are perceived from the perspective of CROSSes (sign 1)
    #in order to update state's Qs for Os, the board hash has to be previously inverted --> in Game class

    ALPHA=0.9
    GAMMA=0.95
    INITIALIZING_VALUE=1 # 1 - optimistic, 0 -pesimistic

    def __init__(self):
        self.state_action_dict=self.generateStatesActionsDict()


    # def initializePesimistic(self):
    #     return [0 for i in range(9)]
    #
    # def initializeOptimistic(self):
    #     return [1 for i in range(9)]

    #Cartesian product
    #TODO think over if cartesian product is necessary -> maybe sytaes collection could be simplified :)
    #creates the matrix in field
    def generateAllStates(self):
        allStates=list(product([-1,0,1],repeat=9))
        allStatesLists=[list(i) for i in allStates]
        return allStatesLists

    def generateStatesActionsDict(self):
        allStatesLists=self.generateAllStates()
        statesActionsDict={}
        for list in allStatesLists:
            q_values=[self.INITIALIZING_VALUE if i==-1 else -1 for i in list]
            statesActionsDict[str(list)]=q_values
        return statesActionsDict

    #TODO verify !!!!
    def updateStateQValues(self,state_hash):
        q_values=self.state_action_dict[state_hash]
        print(q_values)
        max_value=np.max(q_values)
        print(max_value)
        for i in range(len(q_values)):
            if q_values[i] != -1:
                q_values[i]=(1-self.ALPHA)*q_values[i]+self.ALPHA*self.GAMMA*max_value

    def trainOnSingleGame(self,game):
        game.playGame(False)
        for (state,action) in game.player1History:
            #TODO implement
            print(state,action)
        for (state,action) in game.player2History:
            #TODO implement
            print(state,action)

    def trainRandomPlayers(self,gamesCount):
        for i in range(gamesCount):
            board = Board()
            player1 = RandomPlayer("Random1", board, 0)
            player2 = RandomPlayer("Random2", board, 1)
            game = Game(board, player1, player2)
            self.trainOnSingleGame(game)



q_learning=QLearning()
# print(q_learning.state_action_dict)
# print(q_learning.state_action_dict['[-1, 0, 0, -1, 0, 0, -1, 0, 1]'])
# q_learning.updateStateQValues('[-1, 0, 0, -1, 0, 0, -1, 0, 1]')
# print(q_learning.state_action_dict['[-1, 0, 0, -1, 0, 0, -1, 0, 1]'])
q_learning.trainRandomPlayers(10)