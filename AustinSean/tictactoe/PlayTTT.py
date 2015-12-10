__author__ = 'Sean'

from TicTacToe import *
from time import time
from tkinter import *
import menu



class TTTgui:
    def __init__(self, depth = 9):
        self.temp = 0
        self.game = None
        self.player2 = None
        self.buttons = [[None for i in range(0,3)] for j in range(0,3)]
        self.depth = depth


    def play(self):

        # Set up tkinter window
        print("Setting up game...\n")
        self.game = TicTacToe()
        self.player2 = AdversarialSearch(self.game.copy(),"O", self.depth)
        window = Tk()
        window.rowconfigure((0,3), weight=1)
        window.columnconfigure((0,2), weight=1)

        # Setup grid buttons
        for i in range(0,3):
            for j in range(0,3):
                b = Button(window, text = "", pady = 2, width = 5, height = 5, command = lambda a=i,b=j,: self.takeTurn(a,b))
                b.grid(row = i, column = j)
                self.buttons[i][j] = b

        # setup reset button
        buttonR = Button(window, text = "RESET", width = 15, height = 5, command =self.reset)
        buttonR.grid(row = 3, column = 0, columnspan = 3)
        window.mainloop()

    # resets the game
    def reset(self):
        self.game = TicTacToe()
        alpha = -1
        beta = 1
        self.player2 = AdversarialSearch(self.game.copy(),"O", self.depth)
        for i in range(0,3):
            for j in range(0,3):
                self.buttons[i][j]["text"] = ""

    # makes player move, then ai move
    def takeTurn(self, y, x):
        # execute player's move
        if self.game.setPiece(x,y,"X") == -1:
            return
        self.buttons[y][x]["text"] = "X"

        if self.game.isGameOver() != " ":
            status = self.game.isGameOver()

            if status == "TIE":
                print("TIE GAME")
            else:
                print(status + " WINS")
            return

        # execute ai move
        self.player2.state = self.game.copy()
        (t,(x2,y2)) = self.player2.minValue(self.player2.state)
        self.game.setPiece(x2,y2,"O")

        self.buttons[y2][x2]["text"] = "O"

        if self.game.isGameOver() != " ":
            status = self.game.isGameOver()

            if status == "TIE":
                print("TIE GAME")
            else:
                print(status + " WINS")
            return

class TTTgame:
    def __init__(self, depth = 9):
        self.depth = depth

    def play(self):
        # setup board and players
        print("Setting up game...\n")
        game = TicTacToe()

        player1 = AdversarialSearch(game.copy(),"X", self.depth)
        player2 = AdversarialSearch(game.copy(),"O", self.depth)
        while game.isGameOver() == " ":

            # player 1's turn
            print("Player 1 is deciding\n")

            player1.state = game.copy()
            (t,(x1,y1)) = player1.maxValue(player1.state)
            game.setPiece(x1,y1,"X")

            print(game)
            if game.isGameOver() != " ":
                break

            # player 2's turn
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
        # setup board and players
        print("Setting up game...\n")
        game = TicTacToe()
        alpha = -1
        beta = 1
        player1 = AlphaBetaSearch(game.copy(),"X",alpha,beta)
        player2 = AlphaBetaSearch(game.copy(),"O",alpha,beta)
        while game.isGameOver() == " ":
            # player 1's turn
            print("Player 1 is deciding\n")

            player1.state = game.copy()
            (t,(x1,y1)) = player1.maxValueAB(player1.state,alpha,beta)
            game.setPiece(x1,y1,"X")

            print(game)
            if game.isGameOver() != " ":
                break
            # player 2's turn
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


# setup functions that run the games
def runGUI(depth):
    gui = TTTgui(depth)
    gui.play()

def runGame(depth):
    game = TTTgame(depth)
    t0 = time()
    game.play()
    t1 = time()
    print("Time elapsed: ",t1-t0)

def runABGame():
    game = TTTABgame()
    t0 = time()
    game.play()
    t1 = time()
    print("Time elapsed: ",t1-t0)

# menu setup
depth = dict()
title = menu.TextDisplay("Enter the number of the choice to choose it. Enter 'quit' to quit.")
gameChoice = menu.ChoicePrompt("Which game do you want to run?",
                               ["Player vs Adversarial Search", "Adv. Search vs Adv. Search", "AlphaBeta Search vs AlphaBeta Search"])
depthInput = menu.InputPrompt("How deep should the AI search?", int, depth, "depth", lambda x: x >= 0 and x <= 9)
guiRun = menu.FunctionRun(runGUI, depth)
gameRun = menu.FunctionRun(runGame, depth)
ABRun = menu.FunctionRun(runABGame, depth)

titleNode = menu.menuNode(title, [], None)
root = menu.menuNode(gameChoice, [], None)
guiDepth = menu.menuNode(depthInput, [], root)
gameDepth = menu.menuNode(depthInput, [], root)
guiNode = menu.menuNode(guiRun, [], root)
gameNode = menu.menuNode(gameRun, [], root)
ABNode = menu.menuNode(ABRun, [], root)

titleNode.setChildren([root])
root.setChildren([guiDepth, gameDepth, ABNode])
guiDepth.setChildren([guiNode])
gameDepth.setChildren([gameNode])

titleNode.execute()