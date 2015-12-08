__author__ = 'Sean'

class TicTacToe:

    # Initialize board
    def __init__(self):
        self.board = [[" " for i in range(0,3)] for j in range(0,3)]
        self.turn = "X"

    # Print board
    def __str__(self):
        output = ""
        output += (self.turn + "'s turn\n")
        for row in range(0,3):
            for col in range(0,3):
                output += self.board[col][row]
                if col < 2 : output += "|"
            if row < 2 : output += "\n-----\n"
        return output

    # If possible, place piece and switch turns
    def setPiece(self, x, y):
        if self.board[x][y] != " ":
            print("There is already a piece at " + str(x) + "," + str(y))
            return -1
        self.board[x][y] = self.turn


        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"
        return 1

    def getBoard(self):
        return self.board

    def getPiece(self,x,y):
        return self.board[x][y]

    # X wins  , returns 'X'
    # O wins  , returns 'O'
    # Tie     , returns 'TIE'
    # not over, returns ' '
    def isGameOver(self):
        isFull = True
        winner = " "
        b = self.board
        for i in range (0,3):
            for j in range(0,3):
                if b[i][j] == " " : isFull = False

            if b[0][i] == b[1][i] == b[2][i]:
                winner = b[0][i]

            if b[i][0] == b[i][1] == b[i][2]:
                winner = b[i][0]

        if b[0][0] == b[1][1] == b[2][2]:
            winner = b[0][0]
        if b[0][2] == b[1][1] == b[2][0]:
            winner = b[0][2]

        if winner == " " and isFull == True:
            winner = "TIE"

        return winner
