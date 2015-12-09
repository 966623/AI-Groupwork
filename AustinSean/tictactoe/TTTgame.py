__author__ = 'Sean'

from TicTacToe import TicTacToe
import tempSearch

class TTTgame:
    def __init__(self):
        return

    def run(self):
        game = TicTacToe()

        player1 = tempSearch.tempSearch()
        player2 = tempSearch.tempSearch()
        while game.isGameOver() == " ":
            player1.tempTurn()

            if game.isGameOver() != " ":
                break

            player2.tempTurn()

        status = game.isGameOver()

        if status == "TIE":
            print("TIE GAME")
        else:
            print(status + " WINS")