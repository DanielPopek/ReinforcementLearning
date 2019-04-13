from itertools import product
class QLearning(object):
    #assumes that the state-action matrix is a dictionary <stateHash:string, actionsQ:real>
    #actions are in order row by row : [top-lef,top-middle,top-right,middle-left....,down-right]
    #states are perceived from the perspective of CROSSes (sign 1)
    #in order to update state's Qs for Os, the board hash has to be previously inverted --> in Game class

    ALPHA=0.9
    GAMMA=0.95

    def __init__(self):
        self.state_action_dict=self.generateStatesActionsDict()


    def initializePesimistic(self):
        return [0 for i in range(9)]

    def initializeOptimistic(self):
        return [1 for i in range(9)]

    #Cartesian product
    #TODO think over if cartesian product is necessary -> maybe sytaes collection could be simplified :)
    #creates the matrix in field
    def generateAllStates(self):
        allStates=list(product([-1,0,1],repeat=9))
        allStatesHashes=[str(list(i)) for i in allStates]
        return allStatesHashes

    def generateStatesActionsDict(self):
        allStatesHashes=self.generateAllStates()
        statesActionsDict={}
        for hash in allStatesHashes:
            statesActionsDict[hash]=self.initializeOptimistic()
        return statesActionsDict


q_learning=QLearning()
print(q_learning.state_action_dict['[-1, 0, 0, -1, 0, 0, -1, 0, 1]'])