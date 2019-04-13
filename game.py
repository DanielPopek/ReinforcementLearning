from board import Board
from random_player import RandomPlayer
class Game(object):

    def __init__(self,board,player1,player2):
        self.board=board
        self.player1=player1
        self.player2=player2
        self.playerActive=player1
        self.playerInactive=player2

    def switchPlayers(self):
        if self.playerActive==self.player1:
            self.playerActive=self.player2
            self.playerInactive=self.player1
        else:
            self.playerActive=self.player1
            self.playerInactive=self.player2

    def playGame(self):
        move=0
        winner=-1
        while winner==-1 and not self.board.isFull():
            print(f'TURN: {move}')
            action=self.playerActive.nextMove()
            self.board.board[action]=self.playerActive.sign
            self.switchPlayers()
            winner=board.getWinningSign()
            move+=1
        self.board.printBoardFormatted()
        self.board.printBoard()
        if(board.getWinningSign()!=-1):
            sign=self.board.getWinningSign()
            print(f' THE WINNER IS: {self.getWinner(sign)} WITH SIGN {sign}')
        else:
            print('DRAW')

    def getWinner(self,sign):
        if player1.sign==sign:
            return player1.name
        else:
            return player2.name

    def prepareSampleGame(self):
        board= Board()
        player1=RandomPlayer("Random1",board,0)
        player2 = RandomPlayer("Random2", board, 1)
        game=Game(board,player1,player2)
        return game

board= Board()
player1=RandomPlayer("Random1",board,0)
player2 = RandomPlayer("Random2", board, 1)
game=Game(board,player1,player2)

game.playGame()

