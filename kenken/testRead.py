import re
import operator

# Thanks StackOverflow: http://stackoverflow.com/questions/1740726/python-turn-string-into-operator
ops = {'+': operator.add,
       '-': operator.sub,
       '*': operator.mul,
       '/': operator.truediv,
       '==': operator.eq,
       '!=': operator.ne,
       '<': operator.lt,
       '<=': operator.le,
       '>': operator.gt,
       '>=': operator.ge,
       'abs': operator.abs,
       '^': operator.pow
       }

#class struct a bit overkill for this, can use dict[varname]=domain if this is all it needs 
class MakeVar:
    def __init__(self,n,d=[1,2,3,4]):
        self.name = n
        self.domain = d
        
# create a constraint for KenKen specific to number of vars involved
class Constraint:
    def __init__(self,vs,op,a):
        self.nvars = len(vs)
        self.vlist = vs
        self.op = op
        if ( 1 == self.nvars ):
            self.fn = lambda x: x == eval(a)
        elif (2 == self.nvars ):
            self.fn = lambda x,y: ops[op](x,y) == eval(a)
        elif (3 == self.nvars ):
            self.fn = lambda x,y,z: ops[op](ops[op](x,y),z) == eval(a)
        else:
            print('num vars not right')

def readKenKen():

    # read in the file with constraints for KenKen puzzles (1 line per puzzle)
    lines = open('testKenKen.txt').readlines()

    # start a dictionary of variables and a list of constraints
    vars = {}
    Cons = []

    # see https://docs.python.org/3/howto/regex.html
    # check that input is good (testing only the first line). remove all white space first
    r = re.compile('\d+([[]\w+,\W+(,\w+)+[]],*)*')

    testLine = 0 # test this line in file
    l = lines[testLine]
    l=re.sub('[ ]','',l)
    if not r.match(l): return

    # size of puzzle is first number on the line
    n = eval(re.findall('^\d+',l)[0])
    #print('size ',n)
    
    # create a list of constraints (as strings).
    # order is [answer,operator,var+], which can have 1,2, or 3 vars
    # I think I should be able to use 1 regex to capture all as above in match, but couldn't get it working
    cs = []
    c1 = re.findall('[[]\w+,\W+,\w+[]]',l)
    c2 = re.findall('[[]\w+,\W+,\w+,\w+[]]',l)
    c3 = re.findall('[[]\w+,\W+,\w+,\w+,\w+[]]',l)
    cs = c1+c2+c3
    #print('cs ',cs)
    
    # for each of the constraints
    for c in cs:
        # remove white space and brackets, then split constraint into answer,op,var
        c=re.sub('[[\] ]','',c)
        c=re.split(',',c)
        print('c ',c)

        # makeVars if not already in existence
        for v in c[2:len(c)]:
            #print('v ',v)
            if v not in vars:
                vars[v] = MakeVar(v)
        op = c[1]
        answer = c[0]
        # make a constraint
        print(c[2:len(c)])
        Cons.append(Constraint( c[2:len(c)], op, answer ))

    return n,Cons
    #for k in vars:
        #print(k)

    #test the results for line 0
    """if ( testLine == 0 ):
        # 2 var constraint
        c = Cons[0]
        print(c.vlist)
        v1, v2 = vars[c.vlist[0]], vars[c.vlist[1]]
        print(v1.name,'=',v1.domain[3],' ',v2.name,'=',v2.domain[0])
        print('op ', c.fn(v1.domain[3],v2.domain[0]))

        # 3 var constraint
        c = Cons[5]
        v1, v2, v3 = vars[c.vlist[0]], vars[c.vlist[1]], vars[c.vlist[2]]
        print(v1.name,' ',v2.name,' ',v3.name)
        print('op ', c.fn(v1.domain[0],v2.domain[3],v3.domain[1]))"""


if __name__ == "__main__":
    readKenKen()    
