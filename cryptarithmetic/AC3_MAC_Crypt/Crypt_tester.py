__author__ = 'Sean'

import testRead
import AC3_Crypt
import MAC_Crypt
import menu


lineDict = dict()
def setLineRead(line):
    testRead.lineRead = line

def runAC3():
    const = []
    vars = dict()
    AC3_Crypt.setupAC3(const, vars)
    AC3_Crypt.AC3(const, vars, None)

def runMAC():
    op, words, letters = testRead.readCrypt()
    solver = MAC_Crypt.MacCrypt(op, words, letters)
    solution = solver.solve()
    print("\nFinal Solution")
    for k in sorted(solution.keys()):
        print(k, " = ", solution[k].domain[0])

# Makes menu items
mainChoice = menu.ChoicePrompt("Do you want to run AC3 or MAC?", ["AC3", "MAC"])
chooseTest = menu.InputPrompt("Which puzzle, numbers 0 - 6, do you want to run?", int, lineDict, "line",
                              lambda x: int(x) >= 0 and int(x) <= 6)
setLine = menu.FunctionRun(setLineRead, lineDict)
runAC3Test = menu.FunctionRun(runAC3, None)
runMACTest = menu.FunctionRun(runMAC, None)

# Create menu tree
runAC3Node = menu.menuNode(runAC3Test, [])
runMACNode = menu.menuNode(runMACTest, [])
setAC3TestNode = menu.menuNode(setLine, [runAC3Node])
setMACTestNode = menu.menuNode(setLine, [runMACNode])
choseAC3Node = menu.menuNode(chooseTest, [setAC3TestNode])
choseMACNode = menu.menuNode(chooseTest, [setMACTestNode])
mainChoiceNode = menu.menuNode(mainChoice, [choseAC3Node, choseMACNode])

choseAC3Node.setReturnNode(mainChoiceNode)
choseMACNode.setReturnNode(mainChoiceNode)
setAC3TestNode.setReturnNode(choseAC3Node)
setMACTestNode.setReturnNode(choseMACNode)
runAC3Node.setReturnNode(mainChoiceNode)
runMACNode.setReturnNode(mainChoiceNode)

# Run menu
mainChoiceNode.execute()