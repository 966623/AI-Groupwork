__author__ = 'Sean'

from TicTacToe import *
from time import time
from tkinter import *

class TTTgui:
    def __init__(self, depth = 9):
        self.temp = 0
        self.game = None
        self.player2 = None
        self.buttons = [[None for i in range(0,3)] for j in range(0,3)]
        self.depth = depth

    def play(self):
        print("Setting up game...\n")
        alpha = -1
        beta = 1

        self.game = TicTacToe()
        self.player2 = AdversarialSearch(self.game.copy(),"O", self.depth)
        window = Tk()
        window.rowconfigure((0,3), weight=1)
        window.columnconfigure((0,2), weight=1)
        for i in range(0,3):
            for j in range(0,3):
                print(str(i))
                b = Button(window, text = "", pady = 2, width = 5, height = 5, command = lambda a=i,b=j,: self.takeTurn(a,b))
                b.grid(row = i, column = j)
                print(self.buttons)
                self.buttons[i][j] = b


        buttonR = Button(window, text = "RESET", width = 15, height = 5, command =self.reset)
        buttonR.grid(row = 3, column = 0, columnspan = 3)
        window.mainloop()

    def reset(self):
        self.game = TicTacToe()
        alpha = -1
        beta = 1
        self.player2 = AdversarialSearch(self.game.copy(),"O", self.depth)
        for i in range(0,3):
            for j in range(0,3):
                self.buttons[i][j]["text"] = ""

    def takeTurn(self, y, x):
        if self.game.setPiece(x,y,"X") == -1:
            return
        self.buttons[y][x]["text"] = "X"

        print(self.game)
        if self.game.isGameOver() != " ":
            status = self.game.isGameOver()

            if status == "TIE":
                print("TIE GAME")
            else:
                print(status + " WINS")
            return


        self.player2.state = self.game.copy()
        (t,(x2,y2)) = self.player2.minValue(self.player2.state)
        self.game.setPiece(x2,y2,"O")

        self.buttons[y2][x2]["text"] = "O"
        print(self.game)

        if self.game.isGameOver() != " ":
            status = self.game.isGameOver()

            if status == "TIE":
                print("TIE GAME")
            else:
                print(status + " WINS")
            return

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
    def __init__(self, depth = 9):
        self.depth = depth

    def play(self):
        print("Setting up game...\n")
        game = TicTacToe()

        player1 = AdversarialSearch(game.copy(),"X", self.depth)
        player2 = AdversarialSearch(game.copy(),"O", self.depth)
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

g = TTTgame()
h = TTTABgame()
i = TTTDLgame()
p = TTTgui(5)


p.play()

t0 = time()
#g.play()
t1 = time()

t2 = time()
#h.play()
t3 = time()

t4 = time()
#i.play()
t5 = time()

print("reg elapsed: ",t1-t0)
print("AB elapsed: ",t3-t2)
print("DL elapsed: ",t5-t4)