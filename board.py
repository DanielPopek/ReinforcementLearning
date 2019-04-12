
class Board(object):

    #0 ==circle, 1== cross, -1== undefined
    def __init__(self):
        self.board=[-1 for i in range(9)]

    def printBoard(self):
        print(self.board)

    def putSign(self,sign,vectorPosition):
        if(vectorPosition>-1 and vectorPosition<9):
            self.board[vectorPosition]=sign

    def getAllFreePositions(self):
        freePositions=[i for i in range(9) if self.board[i]==-1]
        return freePositions

    def isFull(self):
        freePositions=self.getAllFreePositions()
        return len(freePositions)==0


    #TODO implement

    def checkRow(self,row):
        pass

    def checkRows(self):
        pass

    def checkColumn(self,column):
        pass

    def checkColumns(self):
        pass

    def checkDiagonalLeftUp(self):
        pass

    def checkDiagonalRightUp(self):
        return 1

    def getWinningSign(self):
        winner=-1
        if winner==-1:
            winner=self.checkRows()
        if winner == -1:
            winner = self.checkColumns()
        if winner == -1:
            winner = self.checkDiagonalLeftUp()
        else:
            winner = self.checkDiagonalRightUp()
        return winner


# board= Board()
# board.putSign(1,2)
# board.putSign(0,1)
# board.printBoard()
# print(board.getAllFreePositions())
# print(board.isFull())