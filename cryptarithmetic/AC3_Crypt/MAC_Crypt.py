__author__ = 'Sean'
from testRead import *
import random
import copy
import AC3_Crypt
class MacCrypt:
    # Initialize data
    def __init__(self, op, words, letters):
        self.op = op
        self.words = words
        self.letters = letters
        self.cons = []
        self.vars = dict()

    # Sets up and starts the solver
    def solve(self):
        # Check if solvable
        if len(self.letters) > 10:
            print("Unsolvable, too many letters.")
            return 0

        # Setup variables dictionary, -1 for unassigned letters
        AC3_Crypt.setupAC3(self.cons, self.vars)
        return self.solveRecurse(self.cons, self.vars)

    # Recursive part of the solver
    def solveRecurse(self, constraints, variables):
        # Check if solved
        finished = True
        emptyLetter = " "
        for k in variables.keys():
            for i in variables[k].domain:
                domainCopy = copy.copy(variables[k].domain)
                variables[k].domain = [i]
                state = AC3_Crypt.AC3(constraints, variables)
                if state == -1:
                    return -1
                elif state == 1:
                    return 1
                else:
                    state = self.solveRecurse(constraints, variables)
                    if state == -1:
                        return -1
                    elif state == 1:
                        return 1
                    else:
                        c.domain = copy.copy(domainCopy)


    def testSumSolution(self, variables):
        # Calculate and add up variable values
        sum = 0
        for i in range(len(self.words) - 1):
            word = self.words[i]
            if variables[word[0]]== 0:
                return False
            wordLen = len(word)
            for j in range(wordLen):
                sum += (10**j) * variables[word[wordLen - j - 1]]

        # Calculate and add up solution value
        solution = 0
        word = self.words[len(self.words) - 1]
        if variables[word[0]]== 0:
            return False
        wordLen = len(word)
        for j in range(wordLen):
            solution += (10**j) * variables[word[wordLen - j - 1]]

        # Return whether solution true or false
        if (solution == sum):
            return True
        else:
            return False

op, words, letters = readCrypt()
solver = MacCrypt(op, words, letters)
solution = solver.solve()
print(solution)