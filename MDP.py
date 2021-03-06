# Skyler Martens and Evan Ko
# May 30, 2017
# CSE 415 Final Project

# Provides a representation for Markov Decision Processes
# and functionality for running the transitions between states

# The transition function has three arguments:
# T(s, a, sp), where s and sp are states and a is an action.
# The reward function has the three same
# arguments.  However, its return value is not a probability but
# a numeric reward value.

# operators:  state-space search objects consisting of a precondition
#  and deterministic state-transformation function.
#  For the Rubik's cube, these consist of the 12 quarter turns a player can
#  at any point.

# actions:  objects (for us just Python strings) that are
#  stochastically mapped into operators at runtime according
#  to the Transition function.

import math
import random
import time

REPORTING = False

class MDP:
    def __init__(self):
        self.known_states = set ()
        self.succ = {}
        self.heuristics = {}

    def register_start_state(self, start_state):
        self.start_state = start_state
        self.known_states.add(start_state)

    def register_actions(self, action_list):
        self.actions = action_list

    def register_operators(self, op_list):
        self.ops = op_list

    def register_transition_function(self, transition_function):
        self.T = transition_function

    def register_reward_function(self, reward_function):
        self.R = reward_function

    def random_episode(self, nsteps):
        self.current_state = self.start_state
        self.known_states = set()
        self.known_states.add(self.current_state)
        self.current_reward = 0.0
        for i in range(nsteps):
            self.take_action(random.choice(self.actions))
            if self.current_state == "GAME_OVER":
                print('Terminating at "GAME_OVER" state.')
                break
        if REPORTING: print("Done with "+str(i)+" of random exploration.")
        print("Final state: " + self.current_state)

    def take_action(self, a):
        s = self.current_state
        neighbors = self.state_neighbors(s)
        threshold = 0.0
        rnd = random.uniform(0.0, 1.0)
        r = self.R(s,a,s)
        for sp in neighbors:
            threshold += self.T(s, a, sp)
            if threshold>rnd:
                r = self.R(s, a, sp)
                s = sp
                break
        self.current_state = s
        self.known_states.add(self.current_state)
        if REPORTING: print("After action "+a+", moving to state "+str(self.current_state)+\
                            "; reward is "+str(r))

    def state_neighbors(self, state):
        '''Return a list of the successors of state.  First check
           in the hash self.succ for these.  If there is no list for
           this state, then construct and save it.
           And then return the neighbors.'''
        neighbors = self.succ.get(state, False)
        if neighbors==False:
            neighbors = [op.apply(state) for op in self.ops if op.is_applicable(state)]
            self.succ[state]=neighbors
            self.known_states.update(neighbors)
        return neighbors

    '''def take_action(self, a):
        s = self.current_state
        neighbors = self.state_neighbors(s)
        threshold = 0.0
        rnd = random.uniform(0.0, 1.0)
        r = self.R(s,a,s)
        for sp in neighbors:
            threshold += self.T(s, a, sp)
            if threshold>rnd:
                r = self.R(s, a, sp)
                s = sp
                break
        self.current_state = s
        self.known_states.add(self.current_state)
        if REPORTING: print("After action "+a+", moving to state "+str(self.current_state)+\
                            "; reward is "+str(r))'''

    # populates the set "known_states" with all of the
    # states in a given problem
    def generateAllStates(self):
        current_state = self.start_state
        OPEN = [current_state]
        CLOSED = []
        while OPEN != []:
            curr = OPEN[0]
            del OPEN[0]
            if curr not in CLOSED:
                self.known_states.add(curr)
                CLOSED.append(curr)
                neighbors = self.state_neighbors(curr)
                for element in neighbors:
                    OPEN.append(element)

    # Determines the best action based on a given state
    # and returns that action
    def findMaxMove(self, state):
        action = random.choice(self.actions)
        print(action)
        max_val = -math.inf
        for actions in self.actions:
            cur_val = 0
            cur_tuple = (state, actions)
            cur_val = cur_val + self.QValues.get(cur_tuple)
            for adj in self.state_neighbors(state):
                if cur_tuple in self.QValues:
                    cur_val = cur_val + self.T(state, actions, adj) * (self.calc_heuristic(adj))
            if (cur_val > max_val):
                max_val = cur_val
                action = actions
        return action

    # Function calculates the Q values for each (state, action) tuple
    # based upon Q learning alg
    def QLearning(self, discount, nEpisodes, epsilon):
        self.QValues = {} #hash table to map (state, action) tuples to values
        self.move_times = {} #hash table to map (state, action) tuples to number
                             # times specific tuple evaluated
        self.generateAllStates()
        for states in self.known_states:
            for actions in self.actions:
                s = (states,actions)
                self.QValues.update({s: 0})
                self.move_times.update({s: 0})
        for i in range(nEpisodes):
            temp = random.sample(self.known_states, 1)
            self.current_state = temp[0]
            while self.current_state != "GAME_OVER":
                random_val = round(epsilon * 1000) # anticipate epsilon will only be up to 3 decimals
                rand = random.randrange(1000)
                action = random.choice(self.actions)
                if (rand >= random_val):
                    action = self.findMaxMove(self.current_state)   # Finds optimal move a
                tup = (self.current_state,action)
                adj_states = self.state_neighbors(self.current_state)
                curr_val = 0
                for adj in adj_states:
                    opt_adj_action = self.findMaxMove(adj)  # Finds optimal move a'
                    Qtuple = (adj,opt_adj_action)           #Tuple (s', a')
                    if (adj not in self.known_states):
                       print(len(self.known_states))
                       print("This should never happen")
                    if (Qtuple not in self.QValues):
                        print("PPPPRRRRRRROOOOOOOOBBBBBBBLLLLLLLEEEEEMMMMMM")
                    curr_val = curr_val + self.T(self.current_state, action, adj) * \
                                          (self.R(self.current_state, action, adj) + (
                                          discount * self.QValues.get(Qtuple)))
                num_trials = self.move_times.get(tup)
                num_trials = num_trials + 1;
                self.move_times.update({tup: num_trials})
                curr_tuple_val = self.QValues.get(tup)
                update_tuple_val = ((1 - (1/num_trials)) * curr_tuple_val) + ((1/num_trials) * curr_val)
                self.QValues.update({tup:update_tuple_val})
                self.take_action(action)
                print("The new state is: " + self.current_state)
            print("Solved " + str(i) + " times")

    def calc_heuristic(self, curr_state):
        if (curr_state != "GAME_OVER" and curr_state not in self.heuristics):
            value = 0
            if (curr_state[1] != curr_state[3]) or (curr_state[4] != curr_state[6]):
                    value += 10
            if (curr_state[12] != curr_state[13]) or (curr_state[6] != curr_state[7]):
                    value += 10
            if (curr_state[18] != curr_state[16]) or (curr_state[5] != curr_state[7]):
                    value += 10
            if (curr_state[10] != curr_state[11]) or (curr_state[4] != curr_state[5]):
                    value += 10
            if (curr_state[20] != curr_state[21] or curr_state[21] != curr_state[22] or curr_state[22] != curr_state[23]):
                value += 5
            if (curr_state[0] != curr_state[1] or curr_state[1] != curr_state[2] or curr_state[2] != curr_state[3]):
                value += 3
            if (curr_state[4] != curr_state[5] or curr_state[5] != curr_state[6] or curr_state[6] != curr_state[7]):
                value += 5
            if (curr_state[8] != curr_state[9] or curr_state[9] != curr_state[10] or curr_state[10] != curr_state[11]):
                value += 3
            if (curr_state[12] != curr_state[13] or curr_state[13] != curr_state[14] or curr_state[14] != curr_state[15]):
                value += 3
            if (curr_state[16] != curr_state[17] or curr_state[17] != curr_state[18] or curr_state[18] != curr_state[19]):
                value += 3
            self.heuristics.update({curr_state: (1000 / (value + 1))})
            return (1000 / (value + 1))
        elif curr_state in self.heuristics:
            return self.heuristics.get(curr_state)
        else :
            return 2000

    # Returns the next state based on probability of reaching
    # that state based on current (state, action) pair
    def pickNextState(self, action, currState):
        next_state = []
        adj_states = self.state_neighbors(currState)
        total_prob = 0
        for adj in adj_states:
            if self.T(currState, action, adj) > 0:
                total_prob = total_prob + self.T(currState, action, adj)
                next_state.append([total_prob, adj])
        rand = random.random()
        for i in next_state:
            if (rand <= i[0]):
                return i[1]
        return currState

    # Extracts the optimal action at each location and
    # stores values in dictionary optPolicy
    def extractPolicy(self):
        self.optPolicy = {}
        for state in self.known_states:
            max_val = -math.inf
            for action in self.actions:
                tup = (state, action)
                val = self.QValues.get(tup)
                if (val > max_val):
                    self.optPolicy.update({state: action})
                    max_val = val
