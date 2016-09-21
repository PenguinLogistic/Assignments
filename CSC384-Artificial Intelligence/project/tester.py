from cspbase import *
import itertools
import traceback

import propagators as soln_propagators

#@max_grade(1)
##Checking that importing a course_list with conflicts works as expected.
def model_2_import1(stu_models):
        
	score = 0
	print("---starting scheduler_import1---")
	try:
		course_list = ["300", "369", "343", "418"]
		answer = [['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE', '418'], ['NOCOURSE'], ['NOCOURSE','369'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE', '343'], ['NOCOURSE', '343'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE', '343', '369'], ['NOCOURSE', '343', '369'], ['NOCOURSE', '343', '369'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE', '418'], ['NOCOURSE', '343', '418'], ['NOCOURSE','343', '369'], ['NOCOURSE', '300'], ['NOCOURSE', '300'], ['NOCOURSE', '300'], ['NOCOURSE', '300', '418'], ['NOCOURSE', '300', '418'], ['NOCOURSE', '300', '418'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE', '343'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE', '343'], ['NOCOURSE', '369'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			 ]
		
		csp, var_array = stu_models.weekly_planner_csp(course_list)
		lister = []
		for i in range(5):
			for j in range(24):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 1
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished scheduler_import1---\n")
	return score

##Checking that importing and empty course_list results with an empty variable_array.
def model_2_import2(stu_models):
        
	score = 0
	print("---starting scheduler_import2---")
	try:
		course_list = []
		answer = [['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			 ]
		
		csp, var_array = stu_models.weekly_planner_csp(course_list)
		lister = []
		for i in range(5):
			for j in range(24):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 1
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished scheduler_import2---\n")
	return score


#@max_grade(2)
##Checks that weekly_planner constraints pass when all different, and fail when not all different
def check_model_2_constraints_enum(stu_models):
	score = 2
	print("---starting scheduler_constraints_enum---")
	try:
		course_list = []
		
		csp, var_array = stu_models.weekly_planner_csp(course_list)

		for cons in csp.get_all_cons():
			all_vars = cons.get_scope()
			taken = [] 
			domain_list = [] 
			should_pass = []
			should_fail = [] 
			for va in all_vars:
				domain_list.append(va.cur_domain())
				if len(va.cur_domain()) == 1:
					taken.append(va.cur_domain()[0])
			for i in range(len(all_vars)):
				va = all_vars[i]
				domain = domain_list[i] 
				if len(domain) == 1:
					should_pass.append(domain[0])
					should_fail.append(domain[0])
				else:
					for i in range(1,10):
						if i in domain and i in taken:
							should_fail.append(i)
							break
					for i in range(1,10):
						if i in domain and i not in taken:
							should_pass.append(i)
							taken.append(i)
							break
			if cons.check(should_fail) != cons.check(should_pass):
				if cons.check(should_fail) or not cons.check(should_pass):
					if not cons.check(should_fail):
						print("FAILED\nConstraint %s should be falsified by %r" % (str(cons),should_fail))
						print("var domains:")
						for va in all_vars:
							print(va.cur_domain())
					if cons.check(should_pass):
						print("FAILED\nConstraint %s should be satisfied by %r" % (str(cons),should_pass))
						print("var domains:")
						for va in all_vars:
							print(va.cur_domain())
					print("---finished check_model_2_constraints_enum---\n")
					return 0

	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
		print("---finished scheduler_constraints_enum---\n")
		return 0
	
	print("PASS")
	print("---finished scheduler_constraints_enum---\n")
	return score

#@max_grade(2)
##Checks that weekly_planner constraints are implemented as expected. Check with empty
def check_model_2_constraints1(stu_model):
	score = 0
	print("---starting check_scheduler_constraints1---")
			
	try: 		
		current_list = []
		answer = [['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			 ]
		csp, var_array = stu_model.weekly_planner_csp(current_list)
		lister = [] 		
		soln_propagators.prop_GAC(csp)
		for i in range(5):
			for j in range(24):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 2
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished check_scheduler_constraints1---\n")
	return score

#@max_grade(2)
##Checks that weekly_planner constraints are implemented as expected. Check with conflictions between classes
def check_model_2_constraints2(stu_model):
	score = 0
	print("---starting check_scheduler_constraints2---")
			
	try: 		
		current_list = ["300", "369", "343", "418"]
		answer = [['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
                          ['NOCOURSE', '418'], ['NOCOURSE'], ['NOCOURSE', '369'],\
                          ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
                          ['NOCOURSE', '343'], ['NOCOURSE', '343'],\
                          ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
                          ['NOCOURSE', '343', '369'], ['NOCOURSE', '343', '369'], ['NOCOURSE', '343', '369'],\
                          ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
                          ['NOCOURSE', '418'], ['NOCOURSE', '343', '418'], ['NOCOURSE', '343', '369'], [], ['NOCOURSE', '300'], ['NOCOURSE', '300'], ['NOCOURSE', '300', '418'], ['NOCOURSE', '300', '418'], ['NOCOURSE', '300', '418'],\
                          ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
                          ['NOCOURSE', '343'],\
                          ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
                          ['NOCOURSE', '343'], ['NOCOURSE', '369'],\
                          ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE']]
		csp, var_array = stu_model.weekly_planner_csp(current_list)
		lister = [] 		
		soln_propagators.prop_GAC(csp)
		for i in range(5):
			for j in range(24):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 2
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished check_scheduler_constraints2---\n")
	return score

#@max_grade(2)
##Checks that weekly_planner constraints are implemented as expected. Check with conflictions between classes and with non-real inputs
def check_model_2_constraints3(stu_model):
	score = 0
	print("---starting check_scheduler_constraints3---")
			
	try: 		
		current_list = ["300", "369", "343", "418", "asdf", "notreal"]
		answer = [['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
                          ['NOCOURSE', '418'], ['NOCOURSE'], ['NOCOURSE', '369'],\
                          ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
                          ['NOCOURSE', '343'], ['NOCOURSE', '343'],\
                          ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
                          ['NOCOURSE', '343', '369'], ['NOCOURSE', '343', '369'], ['NOCOURSE', '343', '369'],\
                          ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
                          ['NOCOURSE', '418'], ['NOCOURSE', '343', '418'], ['NOCOURSE', '343', '369'], [], ['NOCOURSE', '300'], ['NOCOURSE', '300'], ['NOCOURSE', '300', '418'], ['NOCOURSE', '300', '418'], ['NOCOURSE', '300', '418'],\
                          ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
                          ['NOCOURSE', '343'],\
                          ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
                          ['NOCOURSE', '343'], ['NOCOURSE', '369'],\
                          ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE']]
		csp, var_array = stu_model.weekly_planner_csp(current_list)
		lister = [] 		
		soln_propagators.prop_GAC(csp)
		for i in range(5):
			for j in range(24):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 2
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished check_scheduler_constraints3---\n")
	return score

#@max_grade(2)
##Checks that weekly_planner constraints are implemented as expected. Check with only with non-real inputs
def check_model_2_constraints4(stu_model):
	score = 0
	print("---starting check_scheduler_constraints4---")
			
	try: 		
		current_list = ["Non-real", "fake_course"]
		answer = [['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'],\
			  ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'], ['NOCOURSE'],\
			 ]
		csp, var_array = stu_model.weekly_planner_csp(current_list)
		lister = [] 		
		soln_propagators.prop_GAC(csp)
		for i in range(5):
			for j in range(24):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 2
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished check_scheduler_constraints4---\n")
	return score

def main(stu_propagators=None, stu_models=None):
	TOTAL_POINTS = 12
	total_score = 0

	import propagators as propagators_soln

	if stu_propagators == None:
		import propagators as stu_propagators
	else:
		import stu_propagators
	if stu_models ==None:
		import weekly_scheduler as stu_models
	else:
		import stu_models
	

	
	total_score += model_2_import1(stu_models)
	total_score += model_2_import2(stu_models)
	total_score += check_model_2_constraints1(stu_models)
	total_score += check_model_2_constraints2(stu_models)
	total_score += check_model_2_constraints3(stu_models)
	total_score += check_model_2_constraints4(stu_models)
	total_score += check_model_2_constraints_enum(stu_models)

	if total_score == TOTAL_POINTS:
		print("Score: %d/%d; Passed all tests" % (total_score,TOTAL_POINTS))
	else:
		print("Score: %d/%d; Did not pass all tests." % (total_score,TOTAL_POINTS))


if __name__=="__main__":
	main()
