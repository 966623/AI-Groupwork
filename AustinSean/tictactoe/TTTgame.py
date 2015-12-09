__author__ = 'Sean'

from TicTacToe import *
from time import time
class TTTgame:
    def __init__(self, none = 0):
        self.temp = 0

    def play(self):
        print("Setting up game...\n")
        game = TicTacToe()

        player1 = AdversarialSearch(game.copy(),"X")
        player2 = AdversarialSearch(game.copy(),"O")
        while game.isGameOver() == " ":

            print("Player 1 is deciding\n")

            player1.state = game.copy()
            (t,(x1,y1)) = player1.maxValue(player1.state)
            game.setPiece(x1,y1,"X")

            print(game)
            if game.isGameOver() != " ":
                break

            print("Player 2 is deciding\n")

            player2.state = game.copy()
            (t,(x2,y2)) = player2.minValue(player2.state)
            game.setPiece(x2,y2,"O")
            print(game)

        status = game.isGameOver()

        if status == "TIE":
            print("TIE GAME")
        else:
            print(status + " WINS")

class TTTABgame:
    def __init__(self, none = 0):
        self.temp = 0

    def play(self):
        print("Setting up game...\n")
        game = TicTacToe()
        alpha = -1
        beta = 1
        player1 = AlphaBetaSearch(game.copy(),"X",alpha,beta)
        player2 = AlphaBetaSearch(game.copy(),"O",alpha,beta)
        while game.isGameOver() == " ":

            print("Player 1 is deciding\n")

            player1.state = game.copy()
            (t,(x1,y1)) = player1.maxValueAB(player1.state,alpha,beta)
            game.setPiece(x1,y1,"X")

            print(game)
            if game.isGameOver() != " ":
                break

            print("Player 2 is deciding\n")

            player2.state = game.copy()
            (t,(x2,y2)) = player2.minValueAB(player2.state,alpha,beta)
            game.setPiece(x2,y2,"O")
            print(game)

        status = game.isGameOver()

        if status == "TIE":
            print("TIE GAME")
        else:
            print(status + " WINS")


class TTTDLgame:
    def __init__(self, none = 0):
        self.temp = 0

    def play(self):
        print("Setting up game...\n")
        game = TicTacToe()
        alpha = -20
        beta = 20
        depth = 0
        player1 = DepthLimitedSearch(game.copy(),"X",alpha,beta,0)
        player2 = DepthLimitedSearch(game.copy(),"O",alpha,beta,0)
        while game.isGameOver() == " ":

            print("Player 1 is deciding\n")

            player1.state = game.copy()
            (t,(x1,y1)) = player1.maxValueDL(player1.state,alpha,beta)
            game.setPiece(x1,y1,"X")

            print(game)
            if game.isGameOver() != " ":
                break

            print("Player 2 is deciding\n")

            player2.state = game.copy()
            (t,(x2,y2)) = player2.minValueDL(player2.state,alpha,beta)
            game.setPiece(x2,y2,"O")
            print(game)

        status = game.isGameOver()

        if status == "TIE":
            print("TIE GAME")
        else:
            print(status + " WINS")

g = TTTgame
h = TTTABgame
i = TTTDLgame

t0 = time()
g.play(g)
t1 = time()

t2 = time()
h.play(h)
t3 = time()

t4 = time()
#i.play(i)
t5 = time()

print("reg elapsed: ",t1-t0)
print("AB elapsed: ",t3-t2)
print("DL elapsed: ",t5-t4)