#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return sudoku CSP models.
'''

from cspbase import *
import itertools

def sudoku_csp_model_1(initial_sudoku_board):

    #domain for blank spaces
    domain = [1,2,3,4,5,6,7,8,9]

    #compute the variable array from the initial sudoku board
    variable_array = []
    for a in range(9):
        sublist = []
        for b in range(9):
            if initial_sudoku_board[a][b] == 0:
                sublist.append(Variable("V{}{}".format(a,b), domain))
            else:
                sublist.append(Variable("V{}{}".format(a,b), [initial_sudoku_board[a][b]]))
            if b == 8:
                variable_array.append(sublist)

    cons = []
    #compute constraints for every row in the sudoku board
    for row in range(9):
        for y in range(9):
            for z in range(y+1,9):
                con = Constraint("C(V{}{},V{}{})".format(row,y,row,z),[variable_array[row][y],variable_array[row][z]])
                sat_tuples = []
                #add satisfying tuples to the constraint
                var1 = con.get_scope()[0]
                var2 = con.get_scope()[1]
                for p in var1.domain():
                    for q in var2.domain():
                        if p != q:
                            sat_tuples.append((p,q))
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    #compute constraints for every column in the sudoku board
    for col in range(9):
        for y in range(9):
            for z in range(y+1,9):
                con = Constraint("C(V{}{},V{}{})".format(y,col,z,col),[variable_array[y][col],variable_array[z][col]])
                #add satisfying tuples to the constraint
                sat_tuples = []
                var1 = con.get_scope()[0]
                var2 = con.get_scope()[1]
                for p in var1.domain():
                    for q in var2.domain():
                        if p != q:
                            sat_tuples.append((p,q))
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    #compute constraints for every 3x3 subsquare in the sudoku board
    for row in range(3):
        for col in range(3):
            #get real row range
            if row == 0:
                coord1 = 3
            elif row == 1:
                coord1 = 6
            else:
                coord1 = 9

            #get real col range
            if col == 0:
                coord2 = 3
            elif col == 1:
                coord2 = 6
            else:
                coord2 = 9
                
            clist = []
            #actual constraint computation
            for j in range(coord1-3,coord1):
                for k in range (coord2-3,coord2):
                    clist.append((j,k))
            for t in itertools.combinations(clist,2):
                a = t[0][0]
                b = t[0][1]
                c = t[1][0]
                d = t[1][1]
                con = Constraint("C(V{}{},V{}{})".format(a,b,c,d), [variable_array[a][b],variable_array[c][d]])
                #add satisfying tuples to the constraint
                sat_tuples = []
                var1 = con.get_scope()[0]
                var2 = con.get_scope()[1]
                for p in var1.domain():
                    for q in var2.domain():
                        if p != q:
                            sat_tuples.append((p,q))
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)    

    #create a variable list from the variable_array for the csp
    varlist = []
    for x in variable_array:
        varlist.extend(x)

    csp = CSP("Model_1", varlist)
    for c in cons:
        csp.add_constraint(c)

    return csp, variable_array
    
    '''Return a CSP object representing a sudoku CSP problem along 
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))

       
       
       The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board
    
       -------------------  
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists
       
       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]
       
       
       This routine returns Model_1 which consists of a variable for
       each cell of the board, with domain equal to {1-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.), then invoke enforce_gac on those
       constraints. All of the constraints of Model_1 MUST BE binary
       constraints (i.e., constraints whose scope includes two and
       only two variables).
    '''
    
#IMPLEMENT

##############################

def sudoku_csp_model_2(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along 
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))

    The input board takes the same input format (a list of 9 lists
    specifying the board as sudoku_csp_model_1.
    
    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables will have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables, then
    invoke enforce_gac on those constraints.
    '''

#IMPLEMENT

    #domain for blank spaces
    domain = [1,2,3,4,5,6,7,8,9]

    #compute the variable array from the initial sudoku board, can be used
    #to get a list of variables for every row
    variable_array = []
    for a in range(9):
        sublist = []
        for b in range(9):
            if initial_sudoku_board[a][b] == 0:
                sublist.append(Variable("V{}{}".format(a,b), domain))
            else:
                sublist.append(Variable("V{}{}".format(a,b), [initial_sudoku_board[a][b]]))
            if b == 8:
                variable_array.append(sublist)

    #compute to find a list of variables for every column 
    column_var_array = []
    for col in range(9):
        collist = []
        for a in range(9):
            collist.append(variable_array[a][col])
            if len(collist) == 9:
                column_var_array.append(collist)

    #compute to find a list of variables for every subsquare
    subsq_var_array = []
    for row in range(3):
        for col in range(3):
            #get real row range
            if row == 0:
                coord1 = 3
            elif row == 1:
                coord1 = 6
            else:
                coord1 = 9

            #get real col range
            if col == 0:
                coord2 = 3
            elif col == 1:
                coord2 = 6
            else:
                coord2 = 9
                
            clist = []
            #actual constraint computation
            for j in range(coord1-3,coord1):
                for k in range (coord2-3,coord2):
                    clist.append(variable_array[j][k])
            subsq_var_array.append(clist)

    cons = []
    #compute constraints for every row in the sudoku board
    for row in range(9):
        con = Constraint("C(All variables of row: {})".format(row), variable_array[row])
        #context list keeps tuples which keep track of the variables with a previously
        #assigned value along with their index in the variable_array[x]
        varDoms = []
        for var in variable_array[row]:
            varDoms.append(var.domain())
        sat_tuples = []
        for t in itertools.product(*varDoms):
            if len(t) == len(set(t)):
                sat_tuples.append(t)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
        
    #compute constraints for every column in the sudoku board
    for col in range(9):
        con = Constraint("C(All variables of column: {})".format(col), column_var_array[col])
        #context list keeps tuples which keep track of the variables with a previously
        #assigned value along with their index in the variable_array[x]
        varDoms = []
        for var in column_var_array[col]:
            varDoms.append(var.domain())
        sat_tuples = []
        for t in itertools.product(*varDoms):
            if len(t) == len(set(t)):
                sat_tuples.append(t)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
               
    #compute constraints for every 3x3 subsquare in the sudoku board
    for subsq in range(9):
        con = Constraint("C(All variables of subsquare: {})".format(subsq), subsq_var_array[subsq])
        #context list keeps tuples which keep track of the variables with a previously
        #assigned value along with their index in the variable_array[x]
        varDoms = []
        for var in subsq_var_array[subsq]:
            varDoms.append(var.domain())
        sat_tuples = []
        for t in itertools.product(*varDoms):
            if len(t) == len(set(t)):
                sat_tuples.append(t)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
        
    #create a variable list from the variable_array for the csp
    varlist = []
    for x in variable_array:
        varlist.extend(x)

    csp = CSP("Model_2", varlist)
    for c in cons:
        csp.add_constraint(c)
    
    return csp, variable_array
    



    
