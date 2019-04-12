class Player(object):
    def __init__(self,name,board,sign):
        self.name=name
        self.board=board
        self.sign=sign

    def nextMove(self):
        return NotImplementedError