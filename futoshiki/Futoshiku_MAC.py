# Sihan Chen
# Project Part 2 : Comparison of CSP and Search Algorithms
# Problem : Futoshiki

import sys
import functools
import queue
from functools import reduce
from testRead import *
import math

############################################################

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
        self.variables, self.constraints = SetupCSP( size )

    def SetupCSP( self, size ):
        ''' This function is used to set up variables and their initial domain. '''
        if size <= 1:
            print( "Unsolvable KenKen")
            sys.exit()
        rows = []
        cols = []
        domain = []
        variables = dict()
        
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
                if ( str(k).startswith(r) ):
                    # Accumulate all ConstraintVars contained in row 'r'
                    aRow.append( variables[k] )
            # Add the allDiff constraints among those row elements
            allDiff( constraints, aRow )
        
        # For example, for cols 1,2,3 (with keys A1,B1,C1 ...) generate A1!=B1!=C1, A2!=B2 ...
        for c in cols:
            aCol = []
            for k in variables.keys():
                key = str(k)
                # The column is indicated in the 2nd character of the key string
                if ( key[1] == c ):
                    # Accumulate all ConstraintVars contained in column 'c'
                    aCol.append( variables[k] )
            allDiff( constraints, aCol )
   
        return variables, constraints


def transferConstraint( cons, csp ):
    for c in cons:
        ctype = c[ 0 ]
        
        # When ctype = 0, constraints are either x < y or x > y 
        if ctype == 0:
            # lvar and rvar are variables on the left side and right side of the comparison operator respectively.
            lvar = c[ 1 ]
            rvar = c[ 2 ]
            bc = BinaryConstraint( csp.variables[ lvar ], csp.variables[ rvar ], c[ 3 ] )
            csp.constraints.append( bc )

        # When ctype = 1, constraints are assignement.
        elif ctype == 1:
            var = c[ 1 ]
            uc = UnaryConstraint( csp.variables[ var ], c[ 2 ] )
            csp.constraints.append( uc )


def MRV( csp ):
    # Select the variable with fewest possible value, that is fewest value in its domain.
    domainLen = []
    for var in csp.variables:
        dlen = len( csp.variables[ var ].domain )
        domainLen.append( ( var, dlen ) )

    # Determine the minimum domain value 
    minVar = domainLen[ 0 ]
    for index in range( 0, len( domainLen ) ):
        if domainLen[ index ][ 1 ] < minVar[ 1 ]:
            minVar = domainLen[ index ]
    return minVar[ 0 ]     

def consistentTest( value, assignment ):
    check = True
    for var in assignment:
        if value = assignment[ var ]:
            check = False
            break
    return check
        
def inference( inferences, csp, var, assignment ):
    
        
def backtracking_search( csp ):
    assignment = dict()
    inferences = dict()
    size, cons = readKenKen()
    return backtrack( inferences, assignment, csp )

def backtrack( inferences, assignment, csp ):
    if completeTest( assignment ):
        return assignment    
    var = MRV( csp )
    for value in var.domain:
        if consistentTest( value, assignment ):
            assignment[ var ] = value 
            inference( inferences, csp, var, assignment )
            if inferences:
                result = backtrack( inferences, assignment, csp )
                if result:
                    return result
    reset( inferences, assignment, csp )
    
                

def Futoshiki():
    size, cons = readFutoshiki()
    csp = CSP( size )
    transferConstraint( cons, csp )


    
        





