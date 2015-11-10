__author__ = 'Sean'
from testRead import *
import time
import copy
class DFSCross:

    def __init__(self, op, var, ans, groupR):
        self.op = op
        self.var = var
        self.varList = []
        self.ans = ans
        self.groupR = groupR
        self.cons = []
        self.vars = dict()
        self.nodesExplored = 0

    def solve(self):

        for a in range(3):
            for b in self.var[a]:
                self.varList.append(b)

        for k in self.varList:
            self.vars[k] = -1
        domain = [x for x in range(1,10)]

        t = time.time()
        sol =  self.DFS(0, domain)
        t = time.time() - t
        print("Time Taken: ", t)
        print("Nodes explored: ", self.nodesExplored)
        return sol

    def DFS(self, varIndex, dom):
        self.nodesExplored += 1
        for i in dom:
            #print("Depth: ", varIndex, i)
            self.vars[self.varList[varIndex]] = i

            if varIndex == len(self.varList) - 1:
                #print("Max Level")
                solved = self.isSolution()
                if solved:
                    #print("Solved")
                    #print(self.vars)
                    return copy.deepcopy(self.vars)
                else:
                    return None

            isValid = self.isSolution()
            if isValid:
                newDom = copy.copy(dom)
                newDom.remove(i)
                result = self.DFS(varIndex + 1, newDom)
                if result != None:
                    return result

        self.vars[self.varList[varIndex]] = -1
        return None

    def isSolution(self):
        valid = True
        opList = self.op

        for i in range(len(opList)):
            if self.vars[self.var[i][0]] != -1 and self.vars[self.var[i][1]] != -1 and self.vars[self.var[i][2]] != -1:
                if self.groupR[i]:

                    if ops[opList[i][0]](self.vars[self.var[i][0]],
                        ops[opList[i][1]](self.vars[self.var[i][1]], self.vars[self.var[i][2]])) != int(self.ans[i]):
                        #print(ops[opList[i][0]](self.vars[self.var[i][0]],
                        #    ops[opList[i][1]](self.vars[self.var[i][1]], self.vars[self.var[i][2]])), self.ans[i])
                        valid = False
                else:
                    if ops[opList[i][1]](ops[opList[i][0]](self.vars[self.var[i][0]], self.vars[self.var[i][1]]),
                        self.vars[self.var[i][2]]) != int(self.ans[i]):
                        #print(ops[opList[i][1]](ops[opList[i][0]](self.vars[self.var[i][0]], self.vars[self.var[i][1]]),
                        #    self.vars[self.var[i][2]]), self.ans[i])
                        valid = False

        return valid
"""
op, var, ans, groupR = readCrossMath()
solver = DFSCross(op, var, ans, groupR)
solution = solver.solve()
print(solution)
"""