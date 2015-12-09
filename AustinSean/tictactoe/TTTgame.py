__author__ = 'Sean'

from TicTacToe import *


class TTTgame:
    def __init__(self):
        return

    def run(self):
        game = TicTacToe()

        player1 = AdversarialSearch(None,None,0,"X")
        player2 = AdversarialSearch(None,None,0,"O")
        while game.isGameOver() == " ":

            (x1,y1) = player1.maxValue(player1.state)
            game.setPiece(x1,y1)

            if game.isGameOver() != " ":
                break

            (x2,y2) = player2.minValue(player2.state)
            game.setPiece(x2,y2)

        status = game.isGameOver()

        if status == "TIE":
            print("TIE GAME")
        else:
            print(status + " WINS")