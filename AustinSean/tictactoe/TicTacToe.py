__author__ = 'Sean'


class AdversarialSearch:
    # Initialize
    def __init__(self, state=None, utility=0, player="X"):

        # State keeps the board, which is a TicTacToe class
        self.state = TicTacToe(state)

        # A list of all possible actions at this state
        # Generated from the state, is a list of (x,y) position tuples
        self.actions = self.state.getSpaces()
        self.utility = utility
        self.player = player  ## The current player at this state (assumed that X goes first)
        # self.terminalTest = terminalTest

#####

    def result(self,state,action):
        newState = state.copy()
        (x,y) = action
        newState.setPiece(x,y,self.player)
        ## Return the state resulting from the current action
        return newState

#####
    ## if the player is X, we choose this function
    def maxValue(self,state):
        bestVal = 0

        # terminalTest
        if self.state.isGameOver() != " ":
            ## Return the utility function value
            return self.utility
        else:
            for action in self.actions:
                min = self.minValue(self.result(state,action))
                if bestVal <= min:
                    bestVal = min
        return bestVal

#####
    ## if the player is O, we choose this function
    def minValue(self,state):
        bestVal = 0

        # terminalTest
        if self.state.isGameOver() != " ":
            ## Return the utility function value
            return self.utility
        else:
            for action in self.actions:
                min = self.maxValue(self.result(state,action))
                if bestVal <= min:
                    bestVal = min
        return bestVal


########################################################################################################################


class TicTacToe:

    # Initialize board
    def __init__(self, first = "X"):
        self.board = [[" " for i in range(0,3)] for j in range(0,3)]
        self.turn = first

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
    def setPiece(self, x, y, piece = " "):
        if self.board[x][y] != " ":
            print("There is already a piece at " + str(x) + "," + str(y))
            return -1

        if piece != " ":
            self.board[x][y] = piece
        else:
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

    # Returns empty spots, which are valid moves
    def getSpaces(self):
        spaceList = []
        for i in range (0,3):
            for j in range(0,3):
                if self.board[i][j] == " ":
                    spaceList.append((i,j))
        return spaceList

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

    # returns copy of board
    def copy(self):
        newBoard = TicTacToe()
        newBoard.board = self.board
        newBoard.turn = self.turn
        return newBoard