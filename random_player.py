from player import Player
import random


class RandomPlayer(Player):
    def __init__(self,name,board,sign):
        Player.__init__(self,name,board,sign)

    def nextMove(self):
        freePositions=self.board.getAllFreePositions()
        decision= random.choice(freePositions)
        print(f' PLAYER: {self.name} plays {self.sign} on position {decision}')
        return decision

