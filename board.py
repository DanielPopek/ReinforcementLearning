import numpy as np

from player import CROSS, OH, UNKNOWN


class Board(object):

    # -1 ==oh, 1== cross, 0== undefined
    def __init__(self):
        self.board = [UNKNOWN for i in range(9)]

    # identifier for state-action dictionary
    def getHash(self):
        return str(self.board)

    # reverts ohs with crosses and returns hash
    def getRevertHash(self):
        # reverted_board = [1 - i if i > -1 else -1 for i in self.board]
        reverted_board = [val * -1 for val in self.board]
        return str(reverted_board)

    def printBoard(self):
        print(self.board)

    def putSign(self, sign, vectorPosition):
        if (vectorPosition > -1 and vectorPosition < 9):
            self.board[vectorPosition] = sign

    def getAllFreePositions(self):
        freePositions = [i for i in range(9) if self.board[i] == UNKNOWN]
        return freePositions

    def isFull(self):
        freePositions = self.getAllFreePositions()
        return len(freePositions) == 0

    def checkRow(self, row):
        brd = self.board
        if (brd[row * 3] == brd[row * 3 + 1] == brd[row * 3 + 2]):
            return brd[row * 3]
        else:
            return UNKNOWN

    def checkRows(self):
        winner = 0
        for i in range(3):
            row_result = self.checkRow(i)
            if row_result != UNKNOWN:
                winner = row_result
        return winner

    def checkColumn(self, column):
        brd = self.board
        if (brd[column] == brd[3 + column] == brd[6 + column]):
            return brd[column]
        else:
            return UNKNOWN

    def checkColumns(self):
        winner = UNKNOWN
        for i in range(3):
            column_result = self.checkColumn(i)
            if column_result != UNKNOWN:
                winner = column_result
        return winner

    def checkDiagonalLeftUp(self):
        brd = self.board
        if (brd[0] == brd[4] == brd[8]):
            return brd[0]
        else:
            return UNKNOWN

    def checkDiagonalRightUp(self):
        brd = self.board
        if (brd[2] == brd[4] == brd[6]):
            return brd[2]
        else:
            return UNKNOWN

    def getWinningSign(self):
        winner = UNKNOWN
        if winner == UNKNOWN:
            winner = self.checkRows()
        if winner == UNKNOWN:
            winner = self.checkColumns()
        if winner == UNKNOWN:
            winner = self.checkDiagonalLeftUp()
        if winner == UNKNOWN:
            winner = self.checkDiagonalRightUp()
        return winner

    def printBoardFormatted(self):
        print()
        board = ["x" if char == CROSS else ("o" if char == OH else " ") for char in self.board]
        # formatted = np.zeros(shape=(3, 3))
        for i in range(3):
            print(board[0 + i*3: 3 + i*3])
        # formatted[0] = np.array(self.board[0:3])
        # formatted[1] = np.array(self.board[3:6])
        # formatted[2] = np.array(self.board[6:])
        # print(formatted)
        # return formatted

