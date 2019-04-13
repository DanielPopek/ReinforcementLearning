from board import Board
from random_player import RandomPlayer
class Game(object):

    #Historia ma postać
    # history=[(stateHash,action),(stateHash,action)..] np. [(233dsw2,2),(232345,1),...]
    def __init__(self,board,player1,player2):
        self.board=board
        self.player1=player1
        self.player2=player2
        self.playerActive=player1
        self.playerInactive=player2
        self.player1History=[]
        self.player2History=[]

    def switchPlayers(self):
        if self.playerActive==self.player1:
            self.playerActive=self.player2
            self.playerInactive=self.player1
        else:
            self.playerActive=self.player1
            self.playerInactive=self.player2

    def putHistoryTuple(self,player,board,action):
        sign=player.sign
        history=self.player1History if player==player1 else self.player2History
        hash=None
        if sign==1:
            hash=board.getHash()
        else:
            hash=board.getRevertHash()
        history.append((hash,action))


    def playGame(self):
        move=0
        winner=-1
        while winner==-1 and not self.board.isFull():
            print(f'TURN: {move}')
            action=self.playerActive.nextMove()
            self.putHistoryTuple(self.playerActive,self.board,action)
            self.board.board[action]=self.playerActive.sign
            self.switchPlayers()
            winner=board.getWinningSign()
            move+=1
        self.board.printBoardFormatted()
        self.board.printBoard()
        if(board.getWinningSign()!=-1):
            sign=self.board.getWinningSign()
            print(f' THE WINNER IS: {self.getWinner(sign).name} WITH SIGN {sign}')
        else:
            print('DRAW')
        print(self.player1History)
        print(self.player2History)

    def getWinner(self,sign):
        if player1.sign==sign:
            return player1
        else:
            return player2

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

