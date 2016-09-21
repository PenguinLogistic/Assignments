'''
Construct and return sudoku CSP models.
'''

from cspbase import *
import itertools

def course_planner_csp(init_board, user_domain):
    #input should be an empty 5x14 board
    domain = ["300N08", "369D11", "369A13", "369N18", "301N18"] #replace this with user_domain later
    days = ["M", "T", "W", "R", "F"];
    daySec = []
    afternoonSec = []
    nightSec = []
    
    for dom in domain:
        if dom[-3] == "D":
            daySec.append(dom)
        elif dom[-3] == "A":
            afternoonSec.append(dom)
        else:
            nightSec.append(dom)
            
    variable_array = []
    for a in range(5):
        sublist = []
        for b in range(8,21):
            if init_board[a][b] != 0:
                #if the board coordinate is predefined, give variable that value
                sublist.append(Variable("{}{}".format(days[a],b), init_board[a][b]))
            else:
                templist = []
                #otherwise fill variable with all possible domain depending on section and timeslot 
                if b < 12:
                    for ts in daySec:
                        if b == int(float(ts[-2:])):
                            templist.append(ts)
                    sublist.append(Variable("{}{}".format(days[a],b), templist))  
                elif b < 18 and b >= 12:
                    for ts in afternoonSec:
                        if b == int(float(ts[-2:])):
                            templist.append(ts)
                    sublist.append(Variable("{}{}".format(days[a],b), templist))
                else:
                    for ts in nightSec:
                        if b == int(float(ts[-2:])):
                            templist.append(ts)
                    sublist.append(Variable("{}{}".format(days[a],b), templist))
        variable_array.append(sublist)
        
    cons = []
    for day in range(5):
        for timeslot in range(8,21):
            varDoms = []
            #split constraint creation depending on sections of the day
            con = Constraint("C:Variables of {}{}".format(days[day], timeslot), variable_array[day][timeslot])
            if not variable_array[day][timeslot]:
                pass
            else:
                for var in variable_array[day][timeslot]:
                    varDoms.append(var.domain())
            #simply create "Satisfying tuples". it is satisfying when no plans
            #overlap at all, so when there is a tuple with only one value.
            sat_tuples = []
            if not varDoms:
                pass
            else:
                for variable in varDoms:
                    if tuple(variable) not in sat_tuples:
                        if len(variable) > 1:
                            for extra in variable:
                                temp2 = [extra]
                                if tuple(temp2) not in sat_tuples:
                                    sat_tuples.append(tuple(temp2))
                    else:
                        sat_tuples.append(tuple(variable))
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)            
    #after making all the constraints, just make the csp.
    varlist = []
    for x in variable_array:
        varlist.extend(x)
    csp = CSP("Schedule CSP", varlist)
    for c in cons:
        csp.add_constraint(c)
    return csp, variable_array

def main():
    course_planner_csp()

if __name__=="__main__":
    main()

