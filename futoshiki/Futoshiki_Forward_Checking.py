# Sihan Chen
# Project Part 2 : Comparison of CSP and Search Algorithms
# Problem : Futoshiki

import sys
import functools
import queue
from functools import reduce
from testRead import *
import math
import copy
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
        self.variables, self.constraints = self.setupCSP( size )
        self.size = size

    def setupCSP( self, size ):
        ''' This function is used to set up variables and their initial domain. '''
        if size <= 1:
            print( "Unsolvable Futoshiki")
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

    def reset( self, var, value, assignment, csp ):
        for variable in assignment[ var ][ 1 ]:
            for l in assignment[ var ][ 1 ][ variable ]:
                csp.variables[ variable ].domain.append( l )
        #csp.variables[ var ].domain.remove( value )
        assignment[ var ][ 0 ] = 0        
        

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
            

def MRV( csp, assignment ):
    # Select the variable with fewest possible value, that is fewest value in its domain.
    domainLen = []
    for var in csp.variables:
        # Only select from unassigned variables
        if ( assignment[ var ][0] == 0 ):
            dlen = len( csp.variables[ var ].domain )
            domainLen.append( ( var, dlen ) )
    print(domainLen)           
    # Determine the minimum domain value

    minVar = domainLen[ 0 ]
    for index in range( 0, len( domainLen ) ):
        if domainLen[ index ][ 1 ] < minVar[ 1 ]:
            minVar = domainLen[ index ]
    return minVar[ 0 ]     


def completeTest( assignment, csp ):
    check = True
    if len( assignment ) != csp.size:
        check = False
    for var in assignment:
        if not( len( assignment[ var ] ) == 1 ):
            check = False
            break
    for c in csp.constraints:
        if ( type( c ) == UnaryConstraint ) and ( c.func( assignment[ c.var1.name ][0] ) == False ) :
            check = False
        elif ( type( c ) == BinaryConstraint ) and \
        ( c.func( assignment[ c.var1.name ][0] , assignment[ c.var2.name ][0] ) == False ) :
            check = False 
    return check    

    
def consistentTest( var, value, csp ):
    check = False
    for c in csp.constraints:
        if ( type( c ) == UnaryConstraint ) and c.var1.name == var and c.func( value ) == False:
                return False    
        """elif ( type( c ) == BinaryConstraint ):
            # Consider var's neighbor
            if c.var2.name == var:
                domain = list( c.var1.domain )
                for x in domain:
                    if c.func( x, value ):
                        check = True
                        break
            elif c.var1.name == var:
                domain = list( c.var2.domain )
                for x in domain:
                    if c.func( value, x ):
                        check = True
                        break"""
    return True        
            

        
def forward_checking( csp, var, assignment ):

    ''' Check all the binary constraint with var as its second variable, that is, establishing
        arc consistency for it.'''
    consist = True
    for c in csp.constraints:
        if ( type( c ) == BinaryConstraint ):
            # Consider var's neighbor
            if c.var2.name == var:
                #print("start checking --------------")
                #print(c.var1.name)
                if c.var1.name not in assignment[ var ][ 1 ]:
                    assignment[ var ][ 1 ][ c.var1.name ] = []
                    #print("assignment0", assignment[ var ][ 0 ])
                    #print("assignment1", assignment[ var ][ 1 ])
                value = assignment[ var ][ 0 ]
                #print("var value",value)
                domain = list( c.var1.domain )
                #print("c.var1. checking domain",domain)
                # For each value in the domain of variable 2
                for x in domain:
                    if c.func( x, value ) == False:
                        c.var1.domain.remove( x )
                        assignment[ var ][ 1 ][ c.var1.name ].append( x )
                print("assignment",c.var1.name, assignment[ var ][ 1 ])
                
                printDomains( csp.variables, 3 )
                if not( c.var1.domain ):
                    print( "checking with empty ------" )
                    consist = False
                    break
    print("end checking without empty -------- ")                
    return consist
    
        
def backtracking_search( csp ):
    assignment = dict()
    # Initialize assignment
    for var in csp.variables:
        assignment[ var ] = ( 0, {} )
    return backtrack( assignment, csp )


def backtrack( assignment, csp ):
    if completeTest( assignment, csp ):
        return assignment    
    var = MRV( csp, assignment )
    print("begin=================")
    print(csp.variables[ var ].name)
    dom = copy.copy( csp.variables[ var ].domain )
    for value in dom:
        print("var",var)
        print("value",value)
        inferences = dict()
        if consistentTest( var, value, csp ):
            assignment[ var ] = [ value, inferences ]
            assignment[ var ][ 1 ][ var ] = []
            varDomain = copy.copy( csp.variables[ var ].domain )
            for val in varDomain:
                if val != value:
                    csp.variables[ var ].domain.remove( val )
                    assignment[ var ][ 1 ][ var ].append( val )
            print(" Before forward_checking 000000000000000000000 "  )
            printDomains( csp.variables, 3 )
            print("after forward_checking ==============xxxxxx")
            check = forward_checking( csp, var, assignment )
            printDomains( csp.variables, 3 ) 
            if check:
                print("check",check)
                result = backtrack( assignment, csp )
                if result != False:
                    return result 
            printDomains( csp.variables, 3 )
            print("daozhe")
            csp.reset( var, value, assignment, csp )
            print("guo le reset")
    return False         
            

def printDomains( vars, size ):
    count = 0
    for k in sorted(vars.keys()):
        print( k,'{',vars[k].domain,'}, ',end="" )
        count = count+1
        if ( 0 == count % size ):
            print(' ')    
                

def Futoshiki():
    size, cons = readFutoshiki()
    csp = CSP( size )
    transferConstraint( cons, csp )
    assignment = backtracking_search( csp )
    printDomains( csp.variables, size )
    print(assignment)

    
        

Futoshiki()



