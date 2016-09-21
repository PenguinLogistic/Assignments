'''
Construct and return sudoku CSP models.
'''

from cspbase import *
from propagators import *
import itertools

def weekly_planner_csp(course_list):
    
    #every CSC course
    total_domain = [\
             ["108", [["A", ["M:1200", "W:1200", "F:1200"]], ["B", ["M:1000", "W:1000", "F:1000"]], ["C", ["M:1300", "W:1300", "F:1300"]], ["D", ["W:1800", "W:1900", "W:2000"]]]],\
             ["148", [["A", ["M:1000", "W:1000", "F:1000"]], ["B", ["M:1400", "W:1400", "F:1400"]]]],\
             ["165", [["A", ["M:1100", "T:0900", "T:1000", "W:1100", "F:1100"]], ["B", ["T:1800", "T:1900", "T:2000", "R:1900", "R:2000"]]]],\
             ["200", [["A", ["M:1500", "W:1500", "F:1500"]]]],\
             ["207", [["A", ["T:1000", "W:1000", "F:1000"]], ["B", ["T:1400", "W:1200", "F:1200"]], ["C", ["F:1300", "F:1400", "F:1500"]], ["D", ["W:1700", "W:1800", "W:1900"]]]],\
             ["209", [["A", ["T:1300", "R:1300", "F:1100"]], ["B", ["T:1300", "R:1300", "F:1200"]]]],\
             ["236", [["A", ["M:1100", "W:1100", "F:1100"]], ["B", ["R:1800", "R:1900", "R:2000"]]]],\
             ["258", [["A", ["T:1800", "W:1900", "F:2000"]], ["B", ["R:1800", "R:1900", "R:2000"]]]],\
             ["263", [["A", ["W:1000", "W:1100", "F:1000"]], ["B", ["W:1400", "W:1500", "F:1300"]]]],\
             ["265", [["A", ["T:1400", "T:1500", "R:1500"]]]],\
             ["300", [["A", ["W:1500", "W:1600", "W:1700"]], ["B", ["W:1800", "W:1900", "W:2000"]]]],\
             ["301", [["A", ["M:1200", "W:1200", "F:1200"]], ["B", ["T:1800", "W:1900", "F:2000"]]]],\
             ["302", [["A", ["M:1600", "W:1600", "F:1600"]]]],\
             ["309", [["A", ["T:1400", "R:1300", "R:1400"]], ["B", ["M:1500", "W:1500", "F:1500"]]]],\
             ["318", [["A", ["T:1000", "R:1000", "R:0900"]], ["B", ["M:1800", "M:1900", "M:2000"]]]],\
             ["324", [["A", ["M:1100", "W:1100", "F:1100"]], ["B", ["R:1800", "R:1900", "R:2000"]]]],\
             ["336", [["A", ["M:1100", "W:1100", "F:1100"]]]],\
             ["343", [["A", ["T:1300", "T:1400", "R:1300"]], ["B", ["W:1300", "W:1400", "F:1300"]], ["C", ["T:1800", "T:1900", "T:2000"]]]],\
             ["369", [["A", ["M:1400", "W:1400", "F:1400"]], ["B", ["T:1800", "T:1900", "T:2000"]]]],\
             ["373", [["A", ["M:1000", "W:1000", "F:1000", "R:1400"]], ["B", ["W:1800", "W:1900", "W:2000", "R:1800"]]]],\
             ["384", [["A", ["T:1300", "R:1300", "R:1400"]]]],\
             ["411", [["A", ["M:1200", "W:1200", "F:1200"]], ["B", ["M:1500", "W:1500", "F:1500"]], ["C", ["R:1800", "R:1900", "R:2000"]]]],\
             ["418", [["A", ["M:1200", "W:1200", "W:1300"]], ["B", ["W:1800", "W:1900", "W:2000"]]]],\
             ["420", [["A", ["T:1500", "R:1500", "R:1600"]]]],\
             ["428", [["A", ["M:1000", "M:1100", "W:1000"]]]],\
             ["436", [["A", ["M:1300", "M:1400", "R:1400"]]]],\
             ["438", [["A", ["M:1600", "W:1600", "F:1200"]]]],\
             ["454", [["A", ["W:1800", "W:1900", "F:2000"]]]],\
             ["456", [["A", ["T:1300", "T:1400", "W:1300"]]]],\
             ["458", [["A", ["T:1300", "T:1400", "F:1300"]], ["B", ["R:1300", "R:1400", "F:1100"]], ["C", ["T:1800", "T:1900", "T:2000"]]]],\
             ["465", [["A", ["R:1800", "R:1900", "R:2000"]]]],\
             ["469", [["A", ["T:1000", "R:1000", "F:1500"]]]],\
             ["485", [["A", ["W:1300", "W:1400", "R:1600"]]]],\
             ["490", [["A", ["R:1800", "R:1900", "R:2000"]]]],\
             ]

    #every timeslot
    init_board = [\
                 ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],\
                 ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],\
                 ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],\
                 ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],\
                 ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']\
                 ]    
    
    days = ["M", "T", "W", "R", "F"]
     
    domain = [["NOCOURSE", []]]

    for course in total_domain:

        course_name = course[0]

        if course_name in course_list:

            domain.append(course)


    #create variable array
    variable_array = []
    for a in range(5):
        
        sublist = []
        
        for b in range(24):
            var_name = days[a] + ":" + init_board[a][b] + "00"
            var_dom = []
            
            for course in domain:
                
                course_name = course[0]
                section_list = course[1]

                if (course_name == "NOCOURSE"):
                    n = course_name
                    var_dom.append(n)
                
                for section in section_list:
                    
                    section_name = section[0]
                    section_hours = section[1]

                    if (var_name in section_hours):
                        n = course_name
                        var_dom.append(n)

            
            var = Variable(var_name, var_dom)
            sublist.append(var)
        
        variable_array.append(sublist)
       
    #create constraints 
    cons = []

    for course in domain:

        course_name = course[0]
        section_list = course[1]

        constraint_scope = []
        c_scope = []

        if not (course_name == "NOCOURSE"):
            sec_count = []
            a = 0

            for section in section_list:

                section_name = section[0]
                section_hours = section[1]

                a += len(section_hours)
                sec_count.append(a)

                c_scope += section_hours


            count = 0

            while count < len(c_scope):
                day = days.index(c_scope[count][0:1])
                hour = int(c_scope[count][2:4])

                constraint_scope.append(variable_array[day][hour])
                count += 1

            constraint = Constraint(course_name, constraint_scope, sec_count)
            cons.append(constraint)

           


    #after making all the constraints, just make the csp.
    varlist = []
    for x in variable_array:
        varlist.extend(x)
    csp = CSP("Schedule CSP", varlist)
    for c in cons:
        csp.add_constraint(c)
    return csp, variable_array


def main():

    #format of domain
    # domain = [nocourse, course_1, course_2, ... , course_n]
    # each course = [course_name, [section_1, section_2, ... , section_n]]
    # each section = [section_name, [timeslot_1, timeslot_2, ... , timeslot_n]]
    # each timeslot is the name of a variable

    course_list = ["300","384","420","418","490", "108", "301"]
    
    csp, variable_array = weekly_planner_csp(course_list)

    bt = BT(csp)
    bt.bt_search(prop_BT)
    bt.print_output()
    print("Output using user's course list of: {}. Checking case that has multiple conflicts".format(course_list))

if __name__=="__main__":
    main()

