__author__ = 'Sean'

from TicTacToe import *

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

g = TTTgame
g.play(g)