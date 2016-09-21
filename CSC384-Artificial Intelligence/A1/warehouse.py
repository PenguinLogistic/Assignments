#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
warehouse STATESPACE 
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint
import copy

##################################################
# The search space class 'warehouse'             #
# This class is a sub-class of 'StateSpace'      #
##################################################

class warehouse(StateSpace):
    def __init__(self, action, gval, plist, slist, time, orders, rstatus, initTime, parent = None):
#IMPLEMENT
        """Initialize a warehouse search state object."""
        StateSpace.__init__(self, action, gval, parent)
        self.plist = plist
        self.slist = slist
        self.time = time
        self.orders = orders
        self.rstatus = rstatus
        self.initTime = initTime

    def successors(self): 
#IMPLEMENT
        '''Return list of warehouse objects that are the successors of the current object'''
        States = list()
        doneRobots = list()
        newRobotList = copy.deepcopy(self.get_robot_status())
        newRobotList2 = copy.deepcopy(self.get_robot_status())
        rListCheck = list()
        newOrderList = copy.deepcopy(self.get_orders())
        busyRobots = list()
        newTime = 0
        rIndex = 0
        cost = -1
        if not self.get_orders():
            #need to find the newtime, new rstatus list 
            for robot in copy.deepcopy(self.get_robot_status()):
                if robot[1] == 'on_delivery':
                    if newTime == 0:
                        newTime = robot[3]
                        doneRobots.append(robot)
                    elif newTime > robot[3]:
                        newTime = robot[3]
                        doneRobots.clear()
                        doneRobots.append(robot)
                    elif newTime == robot[3]:
                        doneRobots.append(robot)
                    else:
                        pass
                else:
                    pass
            '''compute new list to edit robot statuses to idle'''
            for idler in doneRobots:                    
                rIndex = self.get_robot_status().index(idler)
                idler[1] = "idle"
                idler.pop()
                newRobotList[rIndex] = idler
                '''also compute the cost of the action'''
                cost = newTime-self.initTime
            if cost != -1:            
                States.append( warehouse("move_forward({0})".format(newTime), cost, self.plist, self.slist, newTime, self.get_orders(), newRobotList, self.initTime, self) )
            else:
                pass
        else:
            for robit in copy.deepcopy(self.get_robot_status()):
                if robit[1] == "idle":
                    for order in copy.deepcopy(self.get_orders()):
                        newOrderList.remove(order)#note brackets around self.get_orders
                        if not newOrderList:
                            newOrderList = list()
                        newRobot = copy.deepcopy(robit)
                        #print(newRobot)
                        newRobot[1] = "on_delivery" #change robot to on_delivery
                        for product in copy.deepcopy(self.plist):
                            for station in copy.deepcopy(self.slist):
                                if order[0] == product[0] and order[1] == station[0]:
                                    startloc = robit[2]
                                    prodloc = product[1]
                                    stationloc = station[1]
                                    locx = (abs(startloc[0]-prodloc[0]) + abs(prodloc[0]-stationloc[0]))
                                    locy = (abs(startloc[1]-prodloc[1]) + abs(prodloc[1]-stationloc[1]))
                                    totaltime = (locx, locy)
                                    #print(locx)
                                    #print(locy)
                                    newRobot[2] = stationloc #change rstat's location to the finish location
                                    if len(newRobot) > 3:
                                        newRobot = newRobot[0:3]
                                        newRobot.append(totaltime[0] + totaltime[1] + copy.deepcopy(self.get_time()))
                                    else:
                                        newRobot.append(totaltime[0] + totaltime[1] + copy.deepcopy(self.get_time())) #append an extra value for the finish time
                                    for i in copy.deepcopy(self.get_robot_status()):
                                        if i[0] == newRobot[0]:
                                            newRobotList = copy.deepcopy(self.get_robot_status())
                                            newRobotList[newRobotList.index(i)] = newRobot
                                            States.append(warehouse("deliver({0},{1},{2})".format(newRobot[0],product[0],station[0]), self.get_time(), self.plist, self.slist, self.get_time(), newOrderList, newRobotList, self.initTime, self))
                                            newOrderList = copy.deepcopy(self.get_orders())
                                            #print(newRobot)
                                else:
                                    pass
                #append the rest of the busy robots to the busyRobots list
                else:
                    busyRobots.append(robit)
            if not busyRobots:
                pass
            else:
                for robot in copy.deepcopy(busyRobots):
                    if newTime == 0:
                        newTime = robot[3]
                        doneRobots.append(robot)
                    elif newTime > robot[3]:
                        newTime = robot[3]
                        doneRobots.clear()
                        doneRobots.append(robot)
                    elif newTime == robot[3]:
                        doneRobots.append(robot)
                    else:
                        pass
                for idler in copy.deepcopy(doneRobots):
                    rIndex = self.get_robot_status().index(idler)
                    idler[1] = "idle"
                    idler.pop()
                    newRobotList2[rIndex] = idler
                    '''also compute the cost of the action'''
                    cost = newTime-self.initTime
                States.append( warehouse("move_forward({0})".format(newTime), cost, self.plist, self.slist, newTime, self.get_orders(), newRobotList2, self.initTime, self) )
        return States

    def hashable_state(self):
#IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        otuple = []
        rtuple = []
        for o in copy.deepcopy(self.get_orders()):
            otuple.insert(0, tuple(o))
        for r in copy.deepcopy(self.get_robot_status()):
            rtuple.insert(0, tuple(r))        
        return tuple((self.gval, tuple(otuple), tuple(rtuple), self.get_time()))

    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output. 
        #Note that if you implement the "get" routines below properly, 
        #This function should work irrespective of how you represent
        #your state. 

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))
            
        print("Time = {}".format(self.get_time()))
        print("Unfulfilled Orders")
        for o in self.get_orders():
            print("    {} ==> {}".format(o[0], o[1]))
        print("Robot Status")
        for rs in self.get_robot_status():
            print("    {} is {}".format(rs[0], rs[1]), end="")
            if rs[1] == 'idle':
                print(" at location {}".format(rs[2]))
            elif rs[1] == 'on_delivery':
                print(" will be at location {} at time {}".format(rs[2], rs[3]))

#Data accessor routines.

    def get_robot_status(self):
#IMPLEMENT
        return self.rstatus
        '''Return list containing status of each robot
           This list has to be in the format: [rs_1, rs_2, ..., rs_k]
           with one status list for each robot in the state. 
           Each robot status item rs_i is itself a list in the format [<name>, <status>, <loc>, <ftime>]
           Where <name> is the name of the robot (a string)
                 <status> is either the string "idle" or the string "on_delivery"
                 <loc> is a location (a pair (x,y)) 
                       if <status> == "idle" then loc is the robot's current location
                       if <status> == "on_delivery" then loc is the robot's future location
                <ftime> 
                       if <status> == "idle" this item is missing (i.e., the list is of 
                                      length 3)
                       if <status> == "on_delivery" then this is a number that is the 
                                      time that the robot will complete its current delivery
        '''

    def get_time(self):
#IMPLEMENT
        '''Return the current time of this state (a number)'''
        return self.time

    def get_orders(self):
#IMPLEMENT
        return self.orders
        '''Return list of unfulfilled orders of this state
           This list is in the format [o1, o2, ..., om]
           one item for each unfulfilled order. 
           Each oi is itself a list [<product_name>, <packing_station_name>]
           where <product_name> is the name of the product to be delivered
           and  <packing_station_name> is the name of the packing station it is to be delivered to'''

#############################################
# heuristics                                #
#############################################
    
def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0

def heur_min_completion_time(state):
#IMPLEMENT
    '''warehouse heuristic'''
    TIME1 = 0
    t1 = 0
    TIME2 = 0
    t2 = 0
    if not state.get_robot_status():
        pass
    else:
        for rtime in copy.deepcopy(state.get_robot_status()):
            if rtime[1] == "on_delivery":
                t1 = rtime[3] - state.get_time()
                if t1 > TIME1:
                    TIME1 = t1

    if not copy.deepcopy(state.get_orders()):
        pass
    else:
        for otime in copy.deepcopy(state.get_orders()):
            for prod in state.plist:
                for station in state.slist:
                    if otime[0] == prod[0] and otime[1] == station[0]:
                        prodloc = prod[1]
                        stationloc = station[1]
                        coord1 = abs(prodloc[0]-stationloc[0])
                        coord2 = abs(prodloc[1]-stationloc[1])
                        t2 = coord1 + coord2
                        if t2 > TIME2:
                            TIME2 = t2
    return max(TIME1,TIME2)
                
    #We want an admissible heuristic. Since the aim is to deliver all
    #of the products to their packing station in as short as a time as
    #possible. 
    #NOTE that we want an estimate of the ADDED time beyond the current
    #     state time.
    #Consider all of the possible delays in moving from this state to
    #a final delivery of all orders.
    # 1. All robots have to finish any current delivery they are on.
    #    So the earliest we could finish is the 
    #    maximum over all robots on delivery of 
    #       (robot's finish time - the current state time)
    #    we subtract the current state time because we want time
    #    beyond the current time required to complete the delivery
    #    Let this maximum be TIME1.
    #    Clearly we cannot finish before TIME1
    #
    # 2. For all unfulfilled orders we need to pick up the product of
    #    that order with some robot, and then move it to the right
    #    packing station. However, we could do many of these
    #    deliveries in parallel. So to get an *admissible* heuristic
    #    we take the MAXIMUM of a MINUMUM time any unfulfilled order
    #    can be completed. There are many different minimum times that
    #    could be computed...of varying complexity. For simplicity we
    #    ignore the time required to get a robot to package, and
    #    instead take the time to move the package from its location
    #    to the packing station location as being a suitable minimum.
    #    So we compute these minimums, then take the maximum of these
    #    minimums Call this max TIME2
    #    Clearly we cannot finish before TIME2
    #
    # Finally we return as a the heuristic value the MAXIMUM of ITEM1 and ITEM2

def warehouse_goal_fn(state):
#IMPLEMENT
    '''Have we reached the goal when all orders have been delivered'''
    if not state.get_orders():
        for rstate in state.get_robot_status():
            if rstate[1] == "on_delivery":
                return False
        return True
    else:
        return False
            

def make_init_state(product_list, packing_station_list, current_time, open_orders, robot_status):
#IMPLEMENT
    return warehouse("START", 0, product_list, packing_station_list, current_time, open_orders, robot_status, current_time);
    '''Input the following items which specify a state and return a warehouse object 
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       product_list = [p1, p2, ..., pk]
          a list of products. Each product pi is itself a list
          pi = [product_name, (x,y)] where 
              product_name is the name of the product (a string) and (x,y) is the
              location of that product.
       packing_station = [ps1, ps2, ..., psn]
          a list of packing stations. Each packing station ps is itself a list
          pi = [packing_station_name, (x,y)] where 
              packing_station_name is the name of the packing station (a string) and (x,y) is the
              location of that station.
       current_time = an integer >= 0
          The state's current time.
       open_orders = [o1, o2, ..., om] 
          a list of unfulfilled (open) orders. Each order is itself a list
          oi = [product_name, packing_station_name] where
               product_name is the name of the product (a string) and
               packing_station_name is the name of the packing station (a string)
               The order is to move the product to the packing station
        robot_status = [rs1, rs2, ..., rsk]
          a list of robot and their status. Each item is itself a list  
          rsi = ['name', 'idle'|'on_delivery', (x, y), <finish_time>]   
            rsi[0] robot name---a string 
            rsi[1] robot status, either the string "idle" or the string
                  "on_delivery"
            rsi[2] robot's location--if "idle" this is the current robot's
                   location, if "on_delivery" this is the robots final future location
                   after it has completed the delivery
            rsi[3] the finish time of the delivery if the "on_delivery" 
                   this element of the list is absent if robot is "idle" 

   NOTE: for simplicity you may assume that 
         (a) no name (robot, product, or packing station is repeated)
         (b) all orders contain known products and packing stations
         (c) all locations are integers (x,y) where both x and y are >= 0
         (d) the robot status items are correctly formatted
         (e) the future time for any robot on_delivery is >= to the current time
         (f) the current time is >= 0
    '''

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################

def make_rand_init_state(nprods, npacks, norders, nrobots):
    '''Generate a random initial state containing 
       nprods = number of products
       npacks = number of packing stations
       norders = number of unfulfilled orders
       nrobots = number of robots in domain'''

    prods = []
    for i in range(nprods):
        ii = int(i)
        prods.append(["product{}".format(ii), (randint(0,50), randint(0,50))])
    packs = []
    for i in range(npacks):
        ii = int(i)
        packs.append(["packing{}".format(ii), (randint(0,50), randint(0,50))])
    orders = []
    for i in range(norders):
        orders.append([prods[randint(0,nprods-1)][0], packs[randint(0,npacks-1)][0]])
    robotStatus = []
    for i in range(nrobots):
        ii = int(i)
        robotStatus.append(["robot{}".format(ii), "idle", (randint(0,50), randint(0,50))])
    return make_init_state(prods, packs, 0, orders, robotStatus)


def test(nprods, npacks, norders, nrobots):
    s0 = make_rand_init_state(nprods, npacks, norders, nrobots)
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, warehouse_goal_fn, heur_min_completion_time)
