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

def readFutoshiki():

    # read in the file with constraints for KenKen puzzles (1 line per puzzle)
    lines = open('testFutoshiki.txt').readlines()
    testLine = 0 # test this line in file
    l = lines[testLine]
    #remove white space
    l = re.sub('[ ]','',l)
    print('l ',l)

    # size of puzzle is first number on the line
    n = eval(re.findall('^\d+',l)[0])
    l = re.sub('^\d+','',l)
    print('size ',n)
    
    # find all "x Op y" 
    cs=re.findall('\w+\W+\w+',l)
    print('c ',cs)

    # for each, separate apart the variables, operator, and values
    for c in cs:
        # these are x < y OR x > y
        if re.findall('\w+\d+<\w+\d+',c) or re.findall('\w+\d+>\w+\d+',c):
            lvar = re.findall('^\w+\d+',c)[0]
            rvar = re.findall('\w+\d+$',c)[0]
            op = re.findall('\W',c)[0]
            #convert inequalities to lambda fn
            fn = lambda x,y: ops[op](x,y)
            print('lvar,op,rvar,fn(3,4)',lvar,op,rvar,fn(3,4))
        else:
            # find x = value
            if re.findall('\w+\d+=\d+',c):
                var = re.findall('^\w+\d+',c)[0]
                value = re.findall('\d+$',c)[0]
            # find value = x
            elif re.findall('\d+=\w+\d+',c):
                var = re.findall('\w+\d+$',c)[0]
                value = re.findall('^\d+$',c)[0]
            # conver equalities to lambda fn
            fn = lambda x: x == eval(value)
            
            #test results with a print
            print('var,val,fn(1) ',var,'==',value,fn(1))

if __name__ == "__main__":
    readFutoshiki()
