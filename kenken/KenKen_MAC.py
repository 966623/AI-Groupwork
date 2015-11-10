# Sihan Chen
# Project Part 2 : Comparison of CSP and Search Algorithms, KenKen_MAC
# Problem : KenKen

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
        ''' This function is used to set up variables and their initial domain. '''
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

    def reset( self, var, value, assignment, csp ):
        for variable in assignment[ var ][ 1 ]:
            for l in assignment[ var ][ 1 ][ variable ]:
                csp.variables[ variable ].domain.append( l )
        assignment[ var ][ 0 ] = 0        
        

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
            

def MRV( csp, assignment ):
    # Select the variable with fewest possible value, that is fewest value in its domain.
    domainLen = []
    for var in csp.variables:
        # Only select from unassigned variables
        if ( assignment[ var ][0] == 0 ):
            dlen = len( csp.variables[ var ].domain )
            domainLen.append( ( var, dlen ) )
            
    # Determine the minimum domain value

    minVar = domainLen[ 0 ]
    for index in range( 0, len( domainLen ) ):
        if domainLen[ index ][ 1 ] < minVar[ 1 ]:
            minVar = domainLen[ index ]
    return minVar[ 0 ]     


def completeTest( assignment, csp ):
    check = True
    for var in assignment:
        if assignment[ var ][ 0 ] == 0:
            check = False
            return check
    """for c in csp.constraints:
        if ( type( c ) == UnaryConstraint ):
            if assignment[ c.var1.name ][0] == 0:  
                check = False
                return check
            # This branch used to avoid division by zero error.   
            elif c.func( assignment[ c.var1.name ][0] ) == False:
                check = False
                return check
        elif ( type( c ) == BinaryConstraint ):
            if assignment[ c.var1.name ][0] == 0 or assignment[ c.var2.name ][0] == 0:
                check = False
                return check
            # This branch used to avoid division by zero error.  
            elif c.func( assignment[ c.var1.name ][0] , assignment[ c.var2.name ][0] ) == False:
                check = False
                return check"""
    return check   
"""def completeTest( assignment, csp ):
    check = True
    for var in assignment:
        if assignment[ var ][ 0 ] == 0:
            check = False
            return check
    for c in csp.constraints:
        if ( type( c ) == UnaryConstraint ) and ( c.func( assignment[ c.var1.name ][0] ) == False ) :
            check = False
        elif ( type( c ) == BinaryConstraint ) and \
        ( c.func( assignment[ c.var1.name ][0] , assignment[ c.var2.name ][0] ) == False ) :
            check = False 
    return check """
    
def consistentTest( var, value, csp ):
    check = False
    for c in csp.constraints:
        if ( type( c ) == UnaryConstraint ) and c.var1.name == var and c.func( value ) == False:
                return False    
        elif ( type( c ) == BinaryConstraint ):
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
                        break
    return True        

            
def MAC( csp, var, assignment ):
    consist = True
    que = queue.Queue()
    for c in csp.constraints:
        if ( type( c ) == BinaryConstraint ):
            # Consider var's neighbor
            if c.var2.name == var:
                if c.var1.name not in assignment[ var ][ 1 ]:
                    assignment[ var ][ 1 ][ c.var1.name ] = []
                que.put( c )
        elif( type( c ) == TernaryConstraint ):
            # Consider var's neighbor
            if c.var2.name == var or c.var3.name == var:
                if c.var1.name not in assignment[ var ][ 1 ]:
                    assignment[ var ][ 1 ][ c.var1.name ] = []
                que.put( c )
    consist = AC3( csp, que, assignment, var )
    return consist
                       
        
def forward_checking( csp, var, assignment ):

    ''' Check all the binary constraint with var as its second variable, that is, establishing
        arc consistency for it.'''
    consist = True
    for c in csp.constraints:
        if ( type( c ) == BinaryConstraint ):
            # Consider var's neighbor
            if c.var2.name == var:
                if c.var1.name not in assignment[ var ][ 1 ]:
                    assignment[ var ][ 1 ][ c.var1.name ] = []
                value = assignment[ var ][ 0 ]
                domain = list( c.var1.domain )
                # For each value in the domain of variable 2
                for x in domain:
                    if c.func( x, value ) == False:
                        c.var1.domain.remove( x )
                        assignment[ var ][ 1 ][ c.var1.name ].append( x )
                if not( c.var1.domain ):
                    consist = False
                    break               
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
    dom = copy.copy( csp.variables[ var ].domain )
    for value in dom:
        inferences = dict()
        if consistentTest( var, value, csp ):
            assignment[ var ] = [ value, inferences ]
            assignment[ var ][ 1 ][ var ] = []
            varDomain = copy.copy( csp.variables[ var ].domain )
            for val in varDomain:
                if val != value:
                    csp.variables[ var ].domain.remove( val )
                    assignment[ var ][ 1 ][ var ].append( val )
            #print(" before MAC ")
            #printDomains( csp.variables, 3 )
            check = MAC( csp, var, assignment )
            #print(" After MAC ")
            #printDomains( csp.variables, 3 )
            if check:
                result = backtrack( assignment, csp )
                if result != False:
                    return result 
            csp.reset( var, value, assignment, csp )
    return False         
            

def AC3( csp, que, assignment, var ):
    # Initialize the queue by putting all the constraint variables in the queue         
    while not( que.empty() ):
        constr = que.get()
        if Revise( constr, assignment, var ):
            if constr.var1.domain == []:
                return False
            if type( constr ) == BinaryConstraint:
                for constraint in csp.constraints:
                    if type( constraint ) == BinaryConstraint and constraint.var1 != constr.var1 and constraint.var1 != constr.var2 and constraint.var2 == constr.var1:
                        if constraint.var1.name not in assignment[ var ][ 1 ]:
                            assignment[ var ][ 1 ][ constraint.var1.name ] = []
                        que.put( constraint )
                    if type( constraint ) == TernaryConstraint and constraint.var1 != constr.var1 and ( constraint.var2 == constr.var1 or constraint.var3 == constr.var1 ):
                        if constraint.var1.name not in assignment[ var ][ 1 ]:
                            assignment[ var ][ 1 ][ constraint.var1.name ] = []
                        que.put( constraint )                        
            elif type( constr ) == TernaryConstraint:
                for constraint in csp.constraints:                 
                    if type( constraint ) == BinaryConstraint and constraint.var1 != constr.var1 and constraint.var2 == constr.var1:
                        if constraint.var1.name not in assignment[ var ][ 1 ]:
                            assignment[ var ][ 1 ][ constraint.var1.name ] = []
                        que.put( constraint )    
                    if type( constraint ) == TernaryConstraint and constraint.var1 != constr.var1: 
                        if constraint.var1 != constr.var2 and constraint.var1 != constr.var3 and ( constraint.var2 == constr.var1 or constraint.var3 == constr.var1 ):
                            if constraint.var1.name not in assignment[ var ][ 1 ]:
                                assignment[ var ][ 1 ][ constraint.var1.name ] = []
                            que.put( constraint )
                        if ( constraint.var1 == constr.var2 and constraint.var2 == constr.var1 and constraint.var3 != constr.var3 ) or\
                           ( constraint.var1 == constr.var2 and constraint.var2 == constr.var3 and constraint.var3 != constr.var1 ) or\
                           ( constraint.var1 == constr.var3 and constraint.var2 == constr.var1 and constraint.var3 != constr.var2 ) or\
                           ( constraint.var1 == constr.var3 and constraint.var2 == constr.var2 and constraint.var3 != constr.var1 ):
                            if constraint.var1.name not in assignment[ var ][ 1 ]:
                                assignment[ var ][ 1 ][ constraint.var1.name ] = []
                            que.put( constraint )                       
    return True


def Revise( cv, assignment, var ):
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
                assignment[ var ][ 1 ][ cv.var1.name ].append( x )
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
                assignment[ var ][ 1 ][ cv.var1.name ].append( x )
                revised = True        
               

    elif ( type( cv ) == UnaryConstraint ):                                                                              
        dom = list( cv.var1.domain )
        # for each value in the domain of variable
        for x in dom:
            if ( cv.func( x ) == False ):
                cv.var1.domain.remove( x )
                assignment[ var ][ 1 ][ c.var1.name ].append( x )
                revised = True
        
    return revised


def printDomains( vars, size ):
    count = 0
    for k in sorted(vars.keys()):
        print( k,'{',vars[k].domain,'}, ',end="" )
        count = count+1
        if ( 0 == count % size ):
            print(' ')    
                

def KenKen():
    size, cons = readKenKen()
    csp = CSP( size )
    transferConstraint( cons, csp )
    assignment = backtracking_search( csp )
    printDomains( csp.variables, size )

        

KenKen()



