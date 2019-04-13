import numpy as np

class Board(object):

    #0 ==oh, 1== cross, -1== undefined
    def __init__(self):
        self.board=[-1 for i in range(9)]

    #identifier for state-action dictionary
    def getHash(self):
        return str(self.board)

    #reverts ohs with corsses and returns hash
    def getRevertHash(self):
        reverted_board=[1-i if i>-1 else -1 for i in self.board]
        return str(reverted_board)

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
        brd=self.board
        if(brd[row*3]==brd[row*3+1]==brd[row*3+2]):
            return brd[row*3]
        else:
            return -1

    def checkRows(self):
        winner=-1
        for i in range(3):
            row_result=self.checkRow(i)
            if row_result!=-1:
                winner=row_result
        return winner

    def checkColumn(self,column):
        brd = self.board
        if (brd[column] == brd[3+column] == brd[6+column]):
            return brd[column]
        else:
            return -1

    def checkColumns(self):
        winner = -1
        for i in range(3):
            column_result = self.checkColumn(i)
            if column_result != -1:
                winner = column_result
        return winner

    def checkDiagonalLeftUp(self):
        brd = self.board
        if (brd[0] == brd[4] == brd[8]):
            return brd[0]
        else:
            return -1

    def checkDiagonalRightUp(self):
        brd = self.board
        if (brd[2] == brd[4] == brd[6]):
            return brd[2]
        else:
            return -1

    def getWinningSign(self):
        winner=-1
        if winner==-1:
            winner=self.checkRows()
        if winner == -1:
            winner = self.checkColumns()
        if winner == -1:
            winner = self.checkDiagonalLeftUp()
        if winner == -1:
            winner = self.checkDiagonalRightUp()
        return winner

    def printBoardFormatted(self):
        formatted=np.zeros(shape=(3,3))
        formatted[0]=np.array(self.board[0:3])
        formatted[1]=np.array(self.board[3:6])
        formatted[2]=np.array(self.board[6:])
        print(formatted)
        return formatted


# board= Board()
# board.putSign(1,2)
# board.putSign(0,1)
#
# board2= Board()
# board2.putSign(1,2)
# board2.putSign(0,1)
#
#
#
# board.printBoard()
# board.printBoardFormatted()
# print(board.getRevertHash())
# print(board.getAllFreePositions())
# print(board.isFull())
# print(board.getHash()==board2.getHash())