#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one remaining variable)
        we look for unary constraints of the csp (constraints whose scope contains
        only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
         
   '''

import copy

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
    only one uninstantiated variable. Remember to keep 
    track of all pruned variable,value pairs and return '''

    all_pairs = list()
    constraints = csp.get_all_cons()

    #if newVar == None then no variable have been assigned
    if (newVar == None):
      #then look for unary constraints of the csp and forward check these
      for constraint in constraints:
        scope = constraint.get_scope()
        if (len(scope) == 1):
          s, p = fc_check(constraint, scope[0])
          all_pairs += p
          if not s:
            return False, all_pairs

    else:
      #else forward check all constraints with newVar that have 1 unassigned variable left
      for constraint in constraints:
        if constraint.get_n_unasgn() == 1 and (newVar in constraint.get_scope()):
          v = constraint.get_unasgn_vars()
          s, p = fc_check(constraint, v[0])
          all_pairs += p
          #if we see 1 DWO, then we must return False as this configuration does not work
          if not s:
            return False, all_pairs

    return True, all_pairs
      
def fc_check(c, v):
  #c is a constraint with all vars assigned except v
  #function returns status + pruned pairs

  #create list of vals representing variable assignments for other vars in the scope of c
  c_scope = c.get_scope()
  vals = list()
  for variable in c_scope:
    vals.append(variable.get_assigned_value())
    
  pruned = list()

  #loop through current domain of v
  current_domain_v = v.cur_domain()

  for a in current_domain_v:
    
    #create list of values representing variable configuration
    config = copy.deepcopy(vals)
    count = 0      
    while count < len(config):
        if (config[count] == None):
          config[count] = a
          break
        count += 1
    
    #check configuration of variables
    if(not c.check(config)):
      #config is not acceptable, need to prune "a" from curdom of v
      v.prune_value(a)
      #keep track of pruned pair
      pair = (v, a)
      pruned.append(pair)

  if (v.cur_domain_size() == 0):
    #domain wipe out
    return False, pruned
  else:
    #v has values that satisfy the constraint
    return True, pruned 

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    all_pairs = list()
    constraints = csp.get_all_cons()

    if(newVar == None):
      #initialize queue with all constraints
      queue = list()

      for constraint in constraints:
        queue.append(constraint)

      status, pruned = gac_enforce(queue, csp)

    else:
      #initialize queue with constraints that contain newVar in their scope
      queue = list()

      for constraint in constraints:
        if newVar in constraint.get_scope(): 
          queue.append(constraint)

      status, pruned = gac_enforce(queue, csp)
  

    return status, pruned
        

def gac_enforce(queue, csp):

  pruned = list()
  #move through queue of constraints
  while len(queue) > 0:
    c = queue[0]
    queue = queue[1:]
    #loop through vars in scope of constraint
    for var in c.get_scope():
      #loop thorugh vals in domain of the current var
      for d in var.cur_domain():
        scope_vars = c.get_scope()
        scope_vals = [None] * len(scope_vars)
        #get a valid assignment of values with var = d
        #a = get_valid_assignment(c, var, d, scope_vars, scope_vals)
        a = c.has_support(var, d)
        if not a:
          pruned.append((var, d))
          var.prune_value(d)
          #if DWO
          if (var.cur_domain_size() == 0):   
            queue = []
            return False, pruned # DWO
          else: 
            #add all constraints cons st v is in scope(cons) and cons not in queue
            cons_to_add = csp.get_all_cons()
            for cons in cons_to_add:
              if (var in cons.get_scope()) and (cons not in queue):
                queue.append(cons)

    #print("queue")
    #for k in queue:
    #  print(str(k))
    #print("")
  
  return True, pruned
        
def get_valid_assignment(constraint, var, d, scope_vars, scope_vals):

  count = 0

  #loop assigning value d to variable var
  while (count < len(scope_vars)):

    if (str(scope_vars[count]) == str(var)):
      scope_vals[count] = d
      count = 0
      break
    count += 1

  status, implementation = get_valid_assignment_helper(0, constraint, var, scope_vars, scope_vals)
  
  return status

def get_valid_assignment_helper(index, constraint, var, scope_vars, scope_vals):

  if index == len(scope_vals):
    #test scope_vals
    status = constraint.check(scope_vals)
    if status:
      return status, scope_vals
    else:
      return False, []

  elif scope_vars[index] == var:
    #skip this index
    status, implementation = get_valid_assignment_helper(index+1, constraint, var, scope_vars, scope_vals)
    if not status:
      return False, []
    else: 
      return True, implementation

  else:
    #test every value of the var
    curr_dom = scope_vars[index].cur_domain()
    for v in curr_dom:
      scope_vals[index] = v
      status, implementation = get_valid_assignment_helper(index+1, constraint, var, scope_vars, scope_vals)
      if status:
        return status, implementation
    return False, []















    
