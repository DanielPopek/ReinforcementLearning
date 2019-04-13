
class QLearning(object):
    #assumes that the state-action matrix is a dictionary <stateHash:string, actionsQ:real>
    #actions are in order row by row : [top-lef,top-middle,top-right,middle-left....,down-right]
    #states are perceived from the perspective of CROSS
    #in order to update state's Qs for Os, the board hash has to be inverted

    ALPHA=0.9
    GAMMA=0.95

    def __init__(self):
        self.state_action_dict=None

    #creates the matrix in field
    def generateAllStatesActionsMatrix(self):
        return NotImplementedError


