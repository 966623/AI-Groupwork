__author__ = 'Sean'
from testRead import *
import random
import copy
import AC3_Cross
class MacCrypt:
    # Initialize data
    def __init__(self, op, var, ans, groupR):
        self.op = op
        self.var = var
        self.ans = ans
        self.groupR = groupR
        self.cons = []
        self.vars = dict()

    # Sets up and starts the solver
    def solve(self):

        # Setup variables dictionary, -1 for unassigned letters
        AC3_Cross.setupAC3(self.cons, self.vars)
        keys = list(self.vars.keys())
        #keys = sorted(self.vars.keys(), key = lambda x: len(self.vars[x].domain))
        for k in keys:
            print(k, len(self.vars[k].domain))
        return self.backtrace(self.cons, self.vars, keys, 0)

    def backtrace(self, constraints, variables, keys, keyIndex, currentVar = None):
        varCopy = copy.deepcopy(variables)
        state = AC3_Cross.AC3(constraints, varCopy, currentVar)

        if state == -1:
            return None
        if state == 1:
            return varCopy

        keyVal = keys[keyIndex]
        #print(keyVal)
        domain = copy.deepcopy(varCopy[keyVal].domain)

        for d in list(domain):
            varCopy[keyVal].domain = [d]
            state = self.backtrace(constraints, varCopy, keys, keyIndex + 1, varCopy[keyVal])

            if state != None:
                return state

        return None

op, var, ans, groupR = readCrossMath()
solver = MacCrypt(op, var, ans, groupR)
solution = solver.solve()
print("\nFinal Solution")
for k in sorted(solution.keys()):
    print(k, ", ", solution[k].domain)

