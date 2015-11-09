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
        keys = list(self.vars.keys())
        #keys = sorted(self.vars.keys(), key = lambda x: len(self.vars[x].domain))
        #for k in keys:
            #print(k, len(self.vars[k].domain))
        return self.backtrace(self.cons, self.vars, keys, 0)

    def backtrace(self, constraints, variables, keys, keyIndex, currentVar = None):


        varCopy = copy.deepcopy(variables)
        state = AC3_Crypt.AC3(constraints, varCopy, currentVar)

        if state == -1:
            return None
        if state == 1:
            if self.testSumSolution(varCopy):
                return varCopy
            else:
                return None

        keyVal = keys[keyIndex]
        #print(keyVal)
        domain = copy.deepcopy(varCopy[keyVal].domain)

        for d in list(domain):
            varCopy[keyVal].domain = [d]
            state = self.backtrace(constraints, varCopy, keys, keyIndex + 1, varCopy[keyVal])

            if state != None:
                return state

        return None

    def testSumSolution(self, variables):
        # Calculate and add up variable values
        sum = 0
        for i in range(len(self.words) - 1):
            word = self.words[i]
            if variables[word[0]].domain[0]== 0:
                return False
            wordLen = len(word)
            for j in range(wordLen):
                sum += (10**j) * variables[word[wordLen - j - 1]].domain[0]

        # Calculate and add up solution value
        solution = 0
        word = self.words[len(self.words) - 1]
        if variables[word[0]].domain[0]== 0:
            return False
        wordLen = len(word)
        for j in range(wordLen):
            solution += (10**j) * variables[word[wordLen - j - 1]].domain[0]

        # Return whether solution true or false
        if (solution == sum):
            return True
        else:
            return False
"""
op, words, letters = readCrypt()
solver = MacCrypt(op, words, letters)
solution = solver.solve()
print("\nFinal Solution")
for k in sorted(solution.keys()):
    print(k, ", ", solution[k].domain)

"""