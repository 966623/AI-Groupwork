__author__ = 'Sean'


class AdversarialSearch:
    # Initialize
    def __init__(self, state=None, player="X"):

        # State keeps the board, which is a TicTacToe class
        self.state = TicTacToe(state)

        # A list of all possible actions at this state
        # Generated from the state, is a list of (x,y) position tuples
        self.actions = self.state.getSpaces()
        self.player = player  ## The current player at this state (assumed that X goes first)
        # self.terminalTest = terminalTest

#####

    def result(self,state,action, player):
        newState = state.copy()
        (x,y) = action
        newState.setPiece(x,y,player)
        ## Return the state resulting from the current action
        return newState

    def utility(self,status):
        if status == "TIE":
            return 0
        if status == "X":
            return 1
        if status == "O":
            return -1
        return 0
#####

    ## if the player is X, we choose this function
    def maxValue(self,state):
        bestVal = -1
        bestAction = (0,0)
        # terminalTest
        status = state.isGameOver()
        if status != " ":
            ## Return the utility function value

            return (self.utility(status),(0,0))
        else:
            currentActions = state.getSpaces()
            for action in currentActions:
                (max,a) = self.minValue(self.result(state,action,"X"))
                if max > bestVal:
                    bestVal = max
                    bestAction = action
        return (bestVal,bestAction)

#####
    ## if the player is O, we choose this function
    def minValue(self,state):
        bestVal = 1
        bestAction = (0,0)
        # terminalTest
        status = state.isGameOver()
        if status != " ":
            ## Return the utility function value
            return (self.utility(status),(0,0))
        else:
            currentActions = state.getSpaces()
            for action in currentActions:
                (min,a) = self.maxValue(self.result(state,action,"O"))
                if min < bestVal:
                    bestVal = min
                    bestAction = action
        return (bestVal,bestAction)


########################################################################################################################

class AlphaBetaSearch:
    # Initialize
    def __init__(self, state=None, player="X", alpha = -2, beta = 2):

        # State keeps the board, which is a TicTacToe class
        self.state = TicTacToe(state)

        # A list of all possible actions at this state
        # Generated from the state, is a list of (x,y) position tuples
        self.actions = self.state.getSpaces()
        self.player = player  ## The current player at this state (assumed that X goes first)
        self.alpha = alpha
        self.beta = beta

#####


    def result(self,state,action, player):
        newState = state.copy()
        (x,y) = action
        newState.setPiece(x,y,player)
        ## Return the state resulting from the current action
        return newState

    def utility(self,status):
        if status == "TIE":
            return 0
        if status == "X":
            return 1
        if status == "O":
            return -1
        return 0
#####
    ## if the player is X, we choose this function
    def maxValueAB(self,state,alpha,beta):
        bestVal = -1
        bestAction = (0,0)

        # terminalTest
        status = state.isGameOver()
        if status != " ":
            ## Return the utility function value
            return (self.utility(status),(0,0))

        else:
            currentActions = state.getSpaces()
            for action in currentActions:

                (max,a) = self.minValueAB(self.result(state,action,"X"),alpha,beta)

                ## bestVal = MAX(bestVal,max)  ##
                if max > bestVal:             ##
                    bestVal = max              ##
                    bestAction = action        ##
                #################################

                ## alpha = MAX(alpha, bestVal) ##
                if bestVal > alpha:      ##
                    alpha = bestVal       ##
                #################################

                if beta <= alpha:
                    break ## beta cut-off

        return (bestVal,bestAction)

#####
    ## if the player is O, we choose this function
    def minValueAB(self,state,alpha,beta):
        bestVal = 1
        bestAction = (0,0)

        # terminalTest
        status = state.isGameOver()
        if status != " ":
            ## Return the utility function value
            return (self.utility(status),(0,0))

        else:
            currentActions = state.getSpaces()
            for action in currentActions:

                (min,a) = self.maxValueAB(self.result(state,action,"O"),alpha,beta)

                ## bestVal = MIN(bestVal,min) ##
                if min < bestVal:            ##
                    bestVal = min             ##
                    bestAction = action       ##
                ################################

                ## beta = MIN(beta, bestVal) ##
                if bestVal < beta:     ##
                    beta = bestVal      ##
                ###############################

                if beta <= alpha:
                    break ## alpha cut-off

        return (bestVal,bestAction)


########################################################################################################################



class TicTacToe:

    # Initialize board
    def __init__(self, first = "X"):
        self.board = [[" " for i in range(0,3)] for j in range(0,3)]
        self.turn = first

    # Print board
    def __str__(self):
        output = ""
        output += ("\n" + str(self.turn) + "'s turn\n")
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
        b = [[self.board[j][i] for i in range(0,3)] for j in range(0,3)]
        newBoard.board = b
        newBoard.turn = self.turn
        return newBoard

"""
ttt = TicTacToe()
player1 = AdversarialSearch(TicTacToe,"X")
print(player1.maxValue(player1.state))
"""