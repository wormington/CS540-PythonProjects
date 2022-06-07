import copy
from pq import *

"""
    Author: Cade Wormington
    Class: CS 540
    Lecture: 
"""

# A variable holding the goal state for comparison
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# getSucc() takes a state and returns the possible successor states
def getSucc(state):
    puzGrid = []
    zeroLoc = []
    
    row1 = []
    row2 = []
    row3 = []

    # This for loop fills row1, row2, and row3 with their respective values 
    # in the puzzle. They will be used to make a 2D array representation of the puzzle.
    for num in range(3):
        row1.append(state[num])
        row2.append(state[num + 3])
        row3.append(state[num + 6])

        # While the grid is made, the loop also takes note of where the zero tile is.
        if state[num] == 0:
            zeroLoc = [0, num]
        elif state[num + 3] == 0:
            zeroLoc = [1, num]
        elif state[num + 6] == 0:
            zeroLoc = [2, num]

    # The rows are added to a list to make a 2D array
    puzGrid.append(row1)
    puzGrid.append(row2)
    puzGrid.append(row3)

    # succStates holds the possible successor states and succStatesRel holds
    # the successor states relative to the empty tile.
    succStates = []
    succStatesRel = []

    # This finds the successor if the empty tile is moved up, down, left, or right, but
    # leaves out the corners and empty space
    for row in range(-1, 2):
        for col in range(-1, 2):
            if (abs(row) != abs(col)):
                succStatesRel.append([(zeroLoc[0] + row) % 3, (zeroLoc[1] + col) % 3])

    # The copies of the current state are made and the empty space is moved into its possible
    # successor spaces.
    for aStateRel in succStatesRel:
        newGrid = copy.deepcopy(puzGrid)
        newGrid[zeroLoc[0]][zeroLoc[1]] = newGrid[aStateRel[0]][aStateRel[1]]
        newGrid[aStateRel[0]][aStateRel[1]] = 0
        succStates.append(newGrid)

    # returnStates and the loop under it just convert the 2D grid form of the puzzle
    # back to the 1D array form.
    returnStates = []
    for aState in succStates:
        returnStates.append(aState[0] + aState[1] + aState[2])

    # The possible successors are sorted and returned
    list.sort(returnStates)
    return returnStates

# This function uses the above function and returns the successors along 
# with the heuristic value for each
def print_succ(state):
    for state in getSucc(state):
        print(str(state) + " h: " + str(heuristic(state)))

# This function takes a state and returns its heuristic value, which is
# calculated as the number of tiles out of place, excluding the empty (0) tile
def heuristic(state):
    count = 0
    for num in range(9):
        if (GOAL_STATE[num] != state[num]) and (state[num] != 0):
            count += 1
    
    return count

# solve() uses all of the above methods, as well as the A* algorithm to solve the puzzle
# given to it by state
def solve(state):
    # This is the declaration of the open Priority Queue and the closed list for A*
    openPQ = PriorityQueue()
    closed = []

    # The initial state is converted to a state dictionary and enqueued into openPQ
    h0 = heuristic(state)
    s0 = {'state': state, 'h': h0, 'g': 0, 'parent': None, 'f': h0}
    openPQ.enqueue(s0)

    # This while loop continues generating successor states until it finds a path to 
    # the goal state. 
    # finished is the boolean value that stops the loop if a goal is found.
    # currState stores the value of the state most recently popped from openPQ. It is
    # declared outside of the loop so that it can be used to trace a path to a goal once
    # one is found.
    finished = False
    currState = None
    while not finished:
        
        # If openPQ is ever empty, then we are out of successors and the puzzle cannot be solved.
        if openPQ.is_empty():
            print("Error: unable to solve puzzle")
            return

        # The state with the lowest f value is popped into currState and added to the closed list.
        currState = openPQ.pop()
        closed.append(currState['state'])

        # If the popped state is a goal, we set finished to true and break from the while loop.
        if currState['state'] == GOAL_STATE:
            finished = True
            break
    
        # succList is a list of the successor states that can be derived from the current state.
        succList = getSucc(currState['state'])

        # This for loop checks each of the generated successor states to see if they have already
        # been explored. If they have not, they are added to openPQ so that their successors can be
        # generated.
        for successor in succList:
            if successor not in closed:
                openPQ.enqueue({'state': successor, 'h': heuristic(successor), 'g': currState['g'] + 1, 'parent': currState, 'f': heuristic(successor) + currState['g']})
        
    # Once a goal is found and the loop ends, the goal is stored in currState, the state most recently
    # popped from openPQ. currState is used to find the path from the goal state back to the initial
    # state. 
    solveStack = []
    solved = False
    while not solved:
        # currState is added to solveStack. currState's parents are recursively also added to solveStack.
        # This continues until the initial state with no parent is reached.
        solveStack.insert(0, currState)
        if currState['parent'] != None:
            currState = currState['parent']
        else:
            solved = True

    # Lastly, solveStack is iterated through in order to print the moves to reach the goal and each state's
    # heuristic value.
    for move in solveStack:
        print(str(move['state']) + " h: " + str(heuristic(move['state'])) + " moves: " + str(move['g']))
