# Skyler Martens and Evan Ko
# May 30, 2017
# CSE 415 Final Project
# File creates the MDP associated with a 2X2X2 rubik's cube
import random
ACTIONS = ['R', 'L', 'B', 'D', 'F',  'U', 'E']

# g = green, w = white, r = red, y = yellow, b = blue, o = orange
INITIAL_STATE = "WWOOBBGGWWOOGGBBYRYRRYRY"
COLORS = ["ORANGE", "BLUE", "WHITE", "GREEN", "RED", "YELLOW"]
#Each number represents what color in the COLOR the square will start out as
DEFAULT_COLOR_ORIENTATION = (2,2,0,0,1,1,3,3,2,2,0,0,3,3,1,1,5,4,5,4,4,5,4,5)
class Operator:

  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

RightOp = Operator("Move right side towards you 180 degrees",\
                   lambda s:can_move(s,1),\
                   lambda s: apply_move(s, 1))
LeftOp = Operator("Move left side toward you 180 degrees",\
                  lambda s:can_move(s,1),\
                  lambda s: apply_move(s,2))
BackOp = Operator("Move back counter-clockwise 180 degrees",\
                  lambda s:can_move(s,1),\
                  lambda s: apply_move(s,3))
DownOp = Operator("Rotate bottom to the right 180 degress",\
                  lambda s:can_move(s,1),\
                  lambda s: apply_move(s,4))
FrontOp = Operator("Rotate front clockwise 180 degrees",\
                   lambda s:can_move(s,1),\
                   lambda s: apply_move(s,5))
UpperOp = Operator("Rotate top to the left 180 degrees",\
                   lambda s:can_move(s,1),\
                   lambda s: apply_move(s,6))
EndOp = Operator("Go to puzzel over state",\
                 lambda s:can_move(s,2),\
                 lambda s: "GAME_OVER")

OPERATORS = [RightOp, LeftOp, BackOp, DownOp, FrontOp, UpperOp,  EndOp]

# Stores a dictionary of actions to operators
ActionOps = {'R': [RightOp, LeftOp],
             'L': [LeftOp, RightOp],
             'B': [BackOp, FrontOp],
             'D': [DownOp, UpperOp],
             'F': [FrontOp, BackOp],
             'U': [UpperOp, DownOp],
             'E': [EndOp, EndOp]}

def createInitialState():
    global INITIAL_STATE
    requestColors = input("Would you like to customize the colors of your Rubik's Cube? (y/n) ")
    if requestColors is 'y':
        resetInitialStateColors()
        getUserColors()
        fillState()
    describeState(INITIAL_STATE)
    return INITIAL_STATE

def resetInitialStateColors():
    global COLORS
    for i in range(6):
        COLORS[i] = None

# getUserColors:
# This function asks the user to enter colors and sets the mapping of the colors
# allowing it to be used when the cube is drawn on console.
def getUserColors():
    for i in range(6):
        color = input("Please Enter Color " + str(i+1) + ": ").upper()
        while checkIfColorExists(color):
            print("The color has initials that already exist")
            color = input("Please Enter Color " + str(i + 1) + ": ").upper()
        COLORS[i] = color

# checkIfColorExists:
# This function takes a character and checks whether the color has already been
# assigned to the map. If it has, it returns true, else it returns a false.
def checkIfColorExists(color):
    global COLORS
    if color in COLORS:
        return True
    return False

def fillState():
    global INITIAL_STATE, DEFAULT_COLOR_ORIENTATION, COLORS
    temp = list(INITIAL_STATE)
    for i in range(23):
        col = COLORS[DEFAULT_COLOR_ORIENTATION[i]]
        temp[i] = col[0]
    INITIAL_STATE = "".join(temp)

# Returns whether the move is valid
def can_move(s, state_type):
    if state_type == 1 and not is_solved(s):
        return True
    elif state_type == 1 and is_solved(s):
        return False
    elif state_type == 2 and is_solved(s):
        return True
    else:
        return False

def apply_move(s, move):
    sp = ""
    if (move == 7 or s == "GAME_OVER") :
        sp = "GAME_OVER"
    else:
        index_of_side_elements = get_side_elements_moved(move)
        index_of_face_elements = get_face_elements(move)
        side_elements = []
        face_elements = []
        modified_face_elements =[]
        modified_side_elements = []
        array_s = []
        for a in range(24):
            array_s.append(s[a])
        for i in range(8):
            side_elements.append(array_s[index_of_side_elements[i]])
        for j in range(4):
            face_elements.append(array_s[index_of_face_elements[j]])
        modified_face_elements = rotate_right_face(face_elements)
        modified_side_elements = rotate_side_forward(side_elements)
        for k in range(8):
            val = index_of_side_elements[k]
            array_s[val] = modified_side_elements[k]
        for l in range(4):
            val = index_of_face_elements[l]
            array_s[val] = modified_face_elements[l]
        sp = "".join(array_s)
    return sp


# returns all of the side elements affected by move
def get_side_elements_moved(move):
    elements =[]
    if move == 1:
        elements = [9, 11, 5, 7, 13, 15, 20, 22] # move forward 180
    elif move == 2:
        elements = [21, 23, 14, 12, 6, 4, 10, 8] # move forward 180
    elif move == 3:
        elements = [8, 9, 17, 19, 15, 14, 2, 0] # move forward 180
    elif move == 4:
        elements = [23, 22, 19, 18, 7, 6, 3, 2] # move forward 180
    elif move == 5:
        elements =  [1, 3, 12, 13, 18, 16, 11, 10] # move forward 180
    else:
        elements = [0, 1, 4, 5, 16, 17, 20, 21] # move forward 180
    return elements

# moves all elements in array forward by four spaces
def rotate_side_forward(elements):
    new_elements = []
    for i in range(4,8):
        new_elements.append(elements[i])
    for j in range(4):
        new_elements.append(elements[j])
    return new_elements

# Returns all of the face elements affect by rotation
def get_face_elements(move):
    elements =[]
    if move == 1:
        elements = [16,17,18,19]
    elif move == 2:
        elements = [0,1,2,3]
    elif move == 3:
        elements = [20,21,22,23]
    elif move == 4:
        elements = [12,13,14,15]
    elif move == 5:
        elements = [4,5,6,7]
    else:
        elements = [8,9,10,11]
    return elements

# Moves face elements corresponding face rotating to right 180 degrees
def rotate_right_face(elements):
    first = elements[0]
    second = elements[1]
    third = elements[2]
    fourth = elements[3]
    new_elements = [fourth, third, second, first]
    return new_elements


# Returns whether the rubik's cube has been solved
def is_solved(s):
    if len(s) != 24:
        return True
    elif(s[0]==s[1] and s[1]==s[2] and s[2]==s[3] and s[4]==s[5] and s[5]==s[6]\
       and s[6]==s[7] and s[8]==s[9] and s[9]==s[10] and s[10]==s[11] and s[12]==s[13]\
       and s[13] == s[14] and s[14]==s[15] and s[16]==s[17] and s[17]==s[18] and s[18]==s[19] \
       and s[20] == s[21] and s[21]==s[22] and s[22]==s[23]):
        return True
    else:
        return False
    # Stores a dictionary of actions to operators
    ActionOps = {'R': [RightOp, LeftOp, BackOp, FrontOp, UpperOp, DownOp],
                 'L': [LeftOp, RightOp, BackOp, FrontOp, UpperOp, DownOp],
                 'B': [BackOp, FrontOp, RightOp, LeftOp, UpperOp, DownOp],
                 'D': [DownOp, UpperOp, RightOp, LeftOp, BackOp, FrontOp],
                 'F': [FrontOp, BackOp, RightOp, LeftOp, UpperOp, DownOp],
                 'U': [UpperOp, DownOp, RightOp, LeftOp, BackOp, FrontOp],
                 'E': [EndOp, EndOp]}
# Computes the transition probability for going from state s
# to state sp after taking the action a
def T(s,a,sp):
    P_noise = 0.02
    P_noraml = 0.9
    if s=="GAME_OVER": return 0
    if sp=="GAME_OVER":
        if (is_solved(s)): return 1
        else: return 0
    if a =='E' and s==sp: return 0
    if a =='E' and is_solved(s): return 1
    if a == 'E' and not is_solved(s): return 0
    if is_solved(s) and a != 'E': return 0
    if sp == apply_move(s, 1):
        if a=='R': return P_noraml
        if a!='R' or a!= 'E': return P_noise
    if sp == apply_move(s, 2):
        if a=='L': return P_noraml
        if a != 'L' or a != 'E': return P_noise
    if sp == apply_move(s, 3):
        if a=='B': return P_noraml
        if a != 'B' or a != 'E': return P_noise
    if sp == apply_move(s, 4):
        if a=='D': return P_noraml
        if a != 'D' or a != 'E': return P_noise
    if sp == apply_move(s, 5):
        if a=='F': return P_noraml
        if a != 'F' or a != 'E': return P_noise
    if sp == apply_move(s, 6):
        if a=='U': return P_noraml
        if a != 'U' or a != 'E': return P_noise
    if s == sp:
        prob = 0.0
        ops = ActionOps[a]
        if not ops[0].is_applicable(s): prob += P_noraml
        if not ops[1].is_applicable(s): prob += P_noise
        return prob
    return 0


 # Returns the reward associated with transitioning from s to sp via action a.
def R(s, a, sp):
    if s == "GAME_OVER": return 0
    if is_solved(s): return 10000
    return -1  # cost of living

# describeState
# This state takes a state and prints out a visual for the state.
def describeState(state):
    print("         -------")
    for i in range(8, 11, 2):
        print("        | " + state[i] + " | " + state[i+1] + " | ")
    print("---------------------------------")
    line = "| "
    line += state[0] + " | " + state[1] + " | "
    line += state[4] + " | " + state[5] + " | "
    line += state[16] + " | " + state[17] + " | "
    line += state[20] + " | " + state[21] + " | "
    line += "\n"
    line += "| "
    line += state[2] + " | " + state[3] + " | "
    line += state[6] + " | " + state[7] + " | "
    line += state[18] + " | " + state[19] + " | "
    line += state[22] + " | " + state[23] + " | "
    print(line)
    print("---------------------------------")
    for i in range(12, 15, 2):
        print("        | " + state[i] + " | " +  state[i+1] + " | ")
    print("         -------")
