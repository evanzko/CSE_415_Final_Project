# Skyler Martens and Evan Ko
# May 30, 2017
# CSE 415 Final Project
# File creates the MDP associated with a 2X2X2 rubik's cube


ACTIONS = ['R', 'Ri', 'L', 'Li', 'B', 'Bi', 'D', 'Di', 'F', 'Fi', 'U', 'Ui']

# g = green, w = white, r = red, y = yellow, b = blue, o = orange
INITIAL_STATE = ['g','g','g','g','w','w','w','w','r','r','r','r','y','y','y','y','b','b','b','b','o','o','o','o']

class Operator:

  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

RightOp = Operator("Move right side towards you",\
                   lambda s:can_move(s,1),\
                   lambda s: move(s, 1))
RightInvOp = Operator("Move right side away from you",\
                      lambda s:can_move(s,1),\
                      lambda s: move(s, 2))
LeftOp = Operator("Move left side toward you",\
                  lambda s:can_move(s,1),\
                  lambda s: move(s,3))
LeftInvOp = Operator("Move left side away from you",\
                     lambda s:can_move(s,1),\
                     lambda s: move(s,4))
BackOp = Operator("Move back counter-clockwise",\
                  lambda s:can_move(s,1),\
                  lambda s: move(s,5))
BackInvOp = Operator("Move back clockwise",\
                     lambda s:can_move(s,1),\
                     lambda s: move(s,6))
DownOp = Operator("Rotate bottom to the right",\
                  lambda s:can_move(s,1),\
                  lambda s: move(s,7))
DownInvOp = Operator("Rotate bottom to the left",\
                     lambda s:can_move(s,1),\
                     lambda s: move(s,8))
FrontOp = Operator("Rotate front clockwise",\
                   lambda s:can_move(s,1),\
                   lambda s: move(s,9))
FrontInvOp = Operator("Rotate front counter-clockwise",\
                      lambda s:can_move(s,1),\
                      lambda s: move(s,10))
UpperOp = Operator("Rotate top to the left",\
                   lambda s:can_move(s,1),\
                   lambda s: move(s,11))
UpperInvOp = Operator("Rotate top to the right",\
                      lambda s:can_move(s,1),\
                      lambda s: move(s,12))
EndOp = Operator("Go to puzzel over state",\
                 lambda s:can_move(s,2),\
                 lambda s: move(s,13))

OPERATORS = [RightOp, RightInvOp, LeftOp, LeftInvOp, BackOp, BackInvOp,\
             DownOp, DownInvOp, FrontOp, FrontInvOp, UpperOp, UpperInvOp, EndOp]

def can_move(s, state_type):
    if state_type == 1 and not is_solved(s):
        return True
    elif state_type == 1 and is_solved(s):
        return False
    elif state_type == 2 and is_solved(s):
        return True
    else:
        return False

def move(s, move):
    if (move == 13) :
        s = ["GAME_OVER"]
    else:
        index_of_side_elements = get_side_elements_moved(move)
        index_of_face_elements = get_face_elements(move)
        side_elements = []
        face_elements = []
        modified_face_elements =[]
        modified_side_elements = []
        for i in range(8):
            side_elements.append(s[index_of_face_elements[i]])
        for j in range(4):
            face_elements.append(s[index_of_face_elements[j]])
        if (move % 2 == 1):
            modified_face_elements = rotate_right_face(face_elements)
            modified_side_elements = rotate_side_forward(side_elements)
        else:
            modified_side_elements = rotate_side_back(side_elements)
            modified_face_elements = rotate_left_face(face_elements)
        for k in range(8):
            val = index_of_side_elements[k]
            s[val] = modified_side_elements[k]
        for l in range(4):
            val = index_of_face_elements[l]
            s[val] = modified_face_elements[l]


# returns all of the side elements affected by move
def get_side_elements_moved(move):
    elements =[]
    if move == 1:
        elements = [9, 11, 5, 7, 13, 15, 20, 22] # move forward 2
    elif move == 2:
        elements = [9, 11, 5, 7, 13, 15, 20, 22] # move back 2
    elif move == 3:
        elements = [23, 21, 14, 12, 6, 4, 10, 8] # move forward 2
    elif move == 4:
        elements = [23, 21, 14, 12, 6, 4, 10, 8] # move back 2
    elif move == 5:
        elements = [8, 9, 17, 19, 15, 14, 2, 0] # move forward 2
    elif move == 6:
        elements = [8, 9, 17, 19, 15, 14, 2, 0] # move backward 2
    elif move == 7:
        elements = [23, 22, 19, 18, 7, 6, 3, 2] # move forward 2
    elif move == 8:
        elements = [23, 22, 19, 18, 7, 6, 3, 2] # move backward 2
    elif move == 9:
        elements =  [1, 3, 12, 13, 18, 16, 11, 10] # move forward 2
    elif move == 10:
        elements = [1, 3, 12, 13, 18, 16, 11, 10] # move backward 2
    elif move == 11:
        elements = [0, 1, 4, 5, 16, 17, 20, 21] # move forward 2
    else:
        elements = [0, 1, 4, 5, 16, 17, 20, 21] # move back 2
    return elements

# moves all elements in array forward by two spaces
def rotate_side_forward(elements):
    new_elements = []
    for i in range(2,8):
        new_elements.append(elements[i])
    new_elements.append(elements[0])
    new_elements.append(elements[1])
    return new_elements

# moves all elements in array back by two spaces
def rotate_side_back(elements):
    new_elements = []
    new_elements.append(elements[6])
    new_elements.append(elements[7])
    for i in range(6):
        new_elements.append(elements[i])
    return new_elements

# Returns all of the face elements affect by rotation
def get_face_elements(move):
    elements =[]
    if move == 1:
        elements = [16,17,18,19]
    elif move == 2:
        elements = [16,17,18,19]
    elif move == 3:
        elements = [0,1,2,3]
    elif move == 4:
        elements = [0,1,2,3]
    elif move == 5:
        elements = [20,21,22,23]
    elif move == 6:
        elements = [20,21,22,23]
    elif move == 7:
        elements = [12,13,14,15]
    elif move == 8:
        elements = [12,13,14,15]
    elif move == 9:
        elements = [4,5,6,7]
    elif move == 10:
        elements = [4,5,6,7]
    elif move == 11:
        elements = [8,9,10,11]
    else:
        elements = [8,9,10,11]
    return elements

# Moves face elements corresponding face rotating to right
def rotate_right_face(elements):
    first = elements[0]
    second = elements[1]
    third = elements[2]
    fourth = elements[3]
    new_elements = [third, first, fourth, second]
    return new_elements

# Moves face elements corresponding to face rotating to left
def rotate_left_face(elements):
    first = elements[0]
    second = elements[1]
    third = elements[2]
    fourth = elements[3]
    new_elements = [second, fourth, first, third]
    return new_elements


# Returns whether the rubik's cube has been solved
def is_solved(s):
    if(s[0]==s[1] and s[1]==s[2] and s[2]==s[3] and s[4]==s[5] and s[5]==s[6]\
       and s[6]==s[7] and s[8]==s[9] and s[9]==s[10] and s[10]==s[11] and s[12]==s[13]\
       and s[13] == s[14] and s[14]==s[15] and s[16]==s[17] and s[17]==s[18] and s[18]==s[19] \
       and s[20] == s[21] and s[21]==s[22] and s[22]==s[23]):
        return True
    else:
        return False

 # Returns the reward associated with transitioning from s to sp via action a.
def R(s, a, sp):
    if s == ["GAME_OVER"]: return 0
    if is_solved(s): return 10,000
    return 0  # cost of living