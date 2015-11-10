# Sihan Chen
# Project Part 2 : Comparison of CSP and Search Algorithms
# Problem : KenKen

import sys
import functools
import queue
from functools import reduce
from testRead import *

# The primary problem set-up consists of "variables" and "constraints":
#   "variables" are a dictionary of constraint variables (of type ConstraintVar), example variables['A1']
#   "constraints" are a set of binary constraints (of type BinaryConstraint)

# First, Node Consistency is achieved by passing each UnaryConstraint of each variable to nodeConsistent().
# Arc Consistency is achieved by passing "constraints" to Revise().
# AC3 is not fully implemented, Revise() needs to be repeatedly called until all domains are reduced to a single value

class ConstraintVar:
    # instantiation example: ConstraintVar( [1,2,3],'A1' )
    # MISSING filling in neighbors to make it easy to determine what to add to queue when revise() modifies domain
    def __init__( self, d, n ):
        self.domain = [ v for v in d ]
        self.name = n

class UnaryConstraint:
    # v1 is of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiation example: UnaryConstraint( variables['A1'], lambda x: x <= 2 )
    def __init__( self, v1, fn ):
        self.var1 = v1
        self.func = fn

class BinaryConstraint:
    # v1 and v2 should be of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiate example: BinaryConstraint( A1, A2, lambda x,y: x != y )
    def __init__(self, v1, v2, fn):
        self.var1 = v1
        self.var2 = v2
        self.func = fn

class TernaryConstraint:
    # v1, v2 and v3 should be of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiate example: BinaryConstraint( A1, A2, A3 lambda x,y,z: x != y != z )
    def __init__(self, v1, v2, v3, fn):
        self.var1 = v1
        self.var2 = v2
        self.var3 = v3
        self.func = fn
        
def allDiff( constraints, v ):    
    # generate a list of constraints that implement the allDiff constraint for all variable combinations in v
    # constraints is a preconstructed list. v is a list of ConstraintVar instances.
    # call example: allDiff( constraints, [A1,A2,A3] ) will generate BinaryConstraint instances for [[A1,A2],[A2,A1],[A1,A3] ...
    fn = lambda x,y: x != y
    for i in range( len( v ) ):
        for j in range( len( v ) ):
            if ( i != j ) :
                constraints.append( BinaryConstraint( v[ i ], v[ j ], fn ) )

class CSP():
    
    def __init__( self, size ):
        self.variables, self.constraints = self.setupCSP( size )
        self.size = size
      
    def setupCSP( self, size ):
        # This setup is applicable to KenKen and Sudoku. For this example, it is a 3x3 board with each domain initialized to {1,2,3}
        # The VarNames list can then be used as an index or key into the dictionary, ex. variables['A1'] will return the ConstraintVar object

        # Note that I could accomplish the same by hard coding the variables, for example ...
        # A1 = ConstraintVar( [1,2,3],'A1' )
        # A2 = ConstraintVar( [1,2,3],'A2' ) ...
        # constraints.append( BinaryConstraint( A1, A2, lambda x,y: x != y ) )
        # constraints.append( BinaryConstraint( A2, A1, lambda x,y: x != y ) ) ...
        #   but you can see how tedious this would be.
        if size <= 1:
            print( "Unsolvable KenKen")
            sys.exit()
            
        rows = []
        cols = []
        domain = []
        variables = dict()
        constraints = []

        # Creat a list with upper case character in alphabetical order 
        for c in ( chr( i ) for i in range( 65, 65 + size ) ):
            rows.append( c )
            
        # Creat a list with increasing integer from 1 to size 
        for i in range( 1, size+1 ):
            cols.append( str( i ) )

        # Creat a list with initial domain of each variables.
        for i in range( 1, size+1 ):
            domain.append( i )
                       
        # Create name for all the variables, such as A1, A2, A3.....    
        varNames = [ x + y for x in rows for y in cols ]    
        for var in varNames:
            variables[ var ] = ConstraintVar( domain, var )

        for r in rows:
            aRow = []
            for k in variables.keys():
                if ( str( k ).startswith( r ) ):
                    # Accumulate all ConstraintVars contained in row 'r'
                    aRow.append( variables[ k ] )
            # Add the allDiff constraints among those row elements
            allDiff( constraints, aRow )
        
        # For example, for cols 1,2,3 (with keys A1,B1,C1 ...) generate A1!=B1!=C1, A2!=B2 ...
        for c in cols:
            aCol = []
            for k in variables.keys():
                key = str( k )
                # The column is indicated in the 2nd character of the key string
                if ( key[ 1 ] == c ):
                    # Accumulate all ConstraintVars contained in column 'c'
                    aCol.append( variables[ k ] )
            allDiff( constraints, aCol )
   
        return variables, constraints

   
                     
def Revise( cv ):
    revised = False 
    if ( type( cv ) == TernaryConstraint ):
                                                                                                                                                      
        dom1 = list( cv.var1.domain )
        dom2 = list( cv.var2.domain ) 
        dom3 = list( cv.var3.domain )
        # for each value in the domain of variable 1
        for x in dom1:
            check = False
            # for each value in the domain of variable 2
            for y in dom2:
                if y != x:
                    # for each value in the domain of variable 3
                    for z in dom3:
                        if z != y and z != x:    
                        # if nothing in domain of variable2 satisfies the constraint when variable1==x, remove x
                            if not ( cv.func( x, y, z ) == False and cv.func( x, z, y ) == False and cv.func( y, x, z ) == False and cv.func( y, z, x ) == False\
                                and cv.func( z, x, y ) == False and cv.func( z, y, x ) == False ):
                                    check = True
                                    break
            if ( check == False ):
                cv.var1.domain.remove( x )
                revised = True                                    
                    
    elif ( type( cv ) == BinaryConstraint ):
        
        dom1 = list( cv.var1.domain )
        dom2 = list( cv.var2.domain )
        # for each value in the domain of variable 1
        for x in dom1:
            check = False
            # for each value in the domain of variable 2
            for y in dom2:
                if y != x:
                # if nothing in domain of variable2 satisfies the constraint when variable1==x, remove x      
                    if not ( cv.func( x, y ) == False and cv.func( y, x ) == False ):
                        check = True
                        break     
            if ( check == False ):
                cv.var1.domain.remove( x )
                revised = True        
               

    elif ( type( cv ) == UnaryConstraint ):                                                                              
        dom = list( cv.var1.domain )
        # for each value in the domain of variable
        for x in dom:
            if ( cv.func( x ) == False ):
                cv.var1.domain.remove( x )
                revised = True
        
    return revised


def printDomains( vars, size ):
    count = 0
    for k in sorted(vars.keys()):
        print( k,'{',vars[k].domain,'}, ',end="" )
        count = count+1
        if ( 0 == count % size ):
            print(' ')
                                                                    

def transferConstraint( cons, csp ):
    for c in cons:
        num_var = c.nvars
        if num_var == 1:
            uc = UnaryConstraint( csp.variables[ c.vlist[ 0 ] ], c.fn )
            csp.constraints.append( uc )
        elif num_var == 2:
            bc1 = BinaryConstraint( csp.variables[ c.vlist[ 0 ] ], csp.variables[ c.vlist[ 1 ] ], c.fn )
            csp.constraints.append( bc1 )
            bc2 = BinaryConstraint( csp.variables[ c.vlist[ 1 ] ], csp.variables[ c.vlist[ 0 ] ], c.fn )
            csp.constraints.append( bc2 )
        elif num_var == 3:
            tc1 = TernaryConstraint( csp.variables[ c.vlist[ 0 ] ], csp.variables[ c.vlist[ 1 ] ], csp.variables[ c.vlist[ 2 ] ], c.fn )
            csp.constraints.append( tc1 )
            tc2 = TernaryConstraint( csp.variables[ c.vlist[ 1 ] ], csp.variables[ c.vlist[ 0 ] ], csp.variables[ c.vlist[ 2 ] ], c.fn )
            csp.constraints.append( tc2 )
            tc3 = TernaryConstraint( csp.variables[ c.vlist[ 2 ] ], csp.variables[ c.vlist[ 0 ] ], csp.variables[ c.vlist[ 1 ] ], c.fn )
            csp.constraints.append( tc3 )

def AC3( csp, que ):
    # Initialize the queue by putting all the constraint variables in the queue 
    for constraint in csp.constraints:
        que.put( constraint )         
    while not( que.empty() ):
        constr = que.get()
        if Revise( constr ):
            if constr.var1.domain == []:
                return False
            if type( constr ) == BinaryConstraint:
                for constraint in csp.constraints:
                    if type( constraint ) == BinaryConstraint and constraint.var1 != constr.var1 and constraint.var1 != constr.var2 and constraint.var2 == constr.var1:
                        que.put( constraint )
                    if type( constraint ) == TernaryConstraint and constraint.var1 != constr.var1 and ( constraint.var2 == constr.var1 or constraint.var3 == constr.var1 ):
                        que.put( constraint )                        
            elif type( constr ) == TernaryConstraint:
                for constraint in csp.constraints:                 
                    if type( constraint ) == BinaryConstraint and constraint.var1 != constr.var1 and constraint.var2 == constr.var1:
                        que.put( constraint )    
                    if type( constraint ) == TernaryConstraint and constraint.var1 != constr.var1: 
                        if constraint.var1 != constr.var2 and constraint.var1 != constr.var3 and ( constraint.var2 == constr.var1 or constraint.var3 == constr.var1 ):
                            que.put( constraint )
                        if ( constraint.var1 == constr.var2 and constraint.var2 == constr.var1 and constraint.var3 != constr.var3 ) or\
                           ( constraint.var1 == constr.var2 and constraint.var2 == constr.var3 and constraint.var3 != constr.var1 ) or\
                           ( constraint.var1 == constr.var3 and constraint.var2 == constr.var1 and constraint.var3 != constr.var2 ) or\
                           ( constraint.var1 == constr.var3 and constraint.var2 == constr.var2 and constraint.var3 != constr.var1 ):
                            que.put( constraint )
    


def KenKen():
    size, cons = readKenKen()
    csp = CSP( size )
    transferConstraint( cons, csp )
    print("initial domains")
    printDomains( csp.variables, size )
    que = queue.Queue()
    for constraint in csp.constraints:
        que.put( constraint )
    AC3( csp, que )
    print("Domain after AC3")
    printDomains( csp.variables, size )

KenKen()

    
    



