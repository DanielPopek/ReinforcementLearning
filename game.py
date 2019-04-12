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
        while not self.board.isFull():
            print(f'TURN: {move}')
            action=self.playerActive.nextMove()
            self.board.board[action]=self.playerActive.sign
            self.switchPlayers()
            move+=1
        print(self.board.board)
        print(f' THE WINNER IS: {self.getWinner(self.board.getWinningSign())}')

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

