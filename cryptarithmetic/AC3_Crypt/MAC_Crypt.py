__author__ = 'Sean'
from testRead import *
import random
import copy

class MacCrypt:
    def __init__(self, op, words, letters):
        self.op = op
        self.words = words
        self.letters = letters

    def solve(self):
        if len(self.letters) > 10:
            print("Unsolvable, too many letters.")
            return 0
        variables = dict()
        domain = [i for i in range(10)]
        for l in self.letters:
            variables[l] = -1

        return self.solveRecurse(variables, domain)

    def solveRecurse(self, variables, domain):
        finished = True
        emptyLetter = " "
        for k in variables.keys():
            if variables[k] == -1:
                finished = False
                emptyLetter = k

        if finished:
            solved = self.testSumSolution(variables)
            if solved:
                return variables
            else:
                return None
        else:
            for i in domain:
                variables[emptyLetter] = i
                newDomain = copy.copy(domain)
                newDomain.remove(i)
                newVariables = copy.deepcopy(variables)
                print(newDomain)
                print(variables)
                solution = self.solveRecurse(newVariables, newDomain)
                if solution != None:
                    return solution
        return None


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