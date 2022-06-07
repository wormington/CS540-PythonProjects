"""
    Author: Cade Wormington
    Class: CS 540
    Lecture: 
"""

import copy
import random

# succ() generates the valid successors of a given state and returns them as a list.
def succ(state, boulderX, boulderY):
    # succList is the list of possible successors that will be returned.
    succList = []

    # Successors are created by going into each column and moving the queen into each row of the column.
    # States that match the original state are not added as successors. States where a queen conflicts
    # with a boulder are also not added as successors.
    for col in range(len(state)):
        for qRow in range(len(state)):
            if (state[col] != qRow) and not (boulderX == col and boulderY == qRow):
                newState = copy.deepcopy(state)
                newState[col] = qRow
                succList.append(newState)

    # The successor list is sorted before it is returned.
    list.sort(succList)
    return succList

# f() takes a state and returns a score based on how many of its queens are being attacked.
def f(state, boulderX, boulderY):

    # grid is a 2D array representation of our chess board.
    grid = []
    # queenLocs is an array of the [x, y] locations of queens on the chess board. The x and y are
    # in relation to the [0, 0] (top left) of the 2D array above.
    queenLocs = []

    # This for loop converts our state to a game board. In this board, 1's are queens, 0's are empty
    # spaces, and -1's are boulders.
    for row in range(len(state) - 1, -1, -1):
        gameRow = []
        for col in range(len(state)):
            if (state[col] == row):
                gameRow.append(1)
                queenLocs.append([col, (len(state) - 1) - row])
            elif (boulderX == col) and (boulderY == row):
                gameRow.append(-1)
            else:
                gameRow.append(0)
        
        grid.append(gameRow)

    # This for loop checks the score of the board. It goes through queenLocs and determines if each of the
    # queens in the list is being attacked. If a queen is being attacked, the score is incremented and the 
    # next queen is checked. Columns are not checked as there can be no more than 1 queen in a column.
    score = 0
    for queen in queenLocs:
        beingAttacked = False

        # Checks the area to the left of the queen.
        for x in range(queen[0], -1, -1):
            if grid[queen[1]][x] == 1 and queen[0] != x:
                beingAttacked = True
                break
            elif grid[queen[1]][x] == -1:
                break

        if beingAttacked:
            score += 1
            continue

        # Checks the area to the right of the queen.
        for x in range(queen[0], len(state)):
            if grid[queen[1]][x] == 1 and queen[0] != x:
                beingAttacked = True
                break
            elif grid[queen[1]][x] == -1:
                break

        if beingAttacked:
            score += 1
            continue

        # Checks the upward-left diagonal of the queen.
        for num in range(len(state)):
            if (queen[1] - num) > -1 and (queen[0] - num) > -1: 
                if grid[queen[1] - num][queen[0] - num] == 1 and num != 0:
                    beingAttacked = True
                    break
                elif grid[queen[1] - num][queen[0] - num] == -1:
                    break
            else:
                break

        if beingAttacked:
            score += 1
            continue

        # Checks the downward-right diagonal of the queen.
        for num in range(len(state)):
            if (queen[1] + num) < len(state) and (queen[0] + num) < len(state): 
                if grid[queen[1] + num][queen[0] + num] == 1 and num != 0:
                    beingAttacked = True
                    break
                elif grid[queen[1] + num][queen[0] + num] == -1:
                    break
            else:
                break
                
        if beingAttacked:
            score += 1
            continue

        # Checks the upward-right diagonal of the queen.
        for num in range(len(state)):
            if (queen[1] - num) > -1 and (queen[0] + num) < len(state): 
                if grid[queen[1] - num][queen[0] + num] == 1 and num != 0:
                    beingAttacked = True
                    break
                elif grid[queen[1] - num][queen[0] + num] == -1:
                    break
            else:
                break
                
        if beingAttacked:
            score += 1
            continue

        # Checks the downward-left diagonal of the queen.
        for num in range(len(state)):
            if (queen[1] + num) < len(state) and (queen[0] - num) > -1: 
                if grid[queen[1] + num][queen[0] - num] == 1 and num != 0:
                    beingAttacked = True
                    break
                elif grid[queen[1] + num][queen[0] - num] == -1:
                    break
            else:
                break
                
        if beingAttacked:
            score += 1
            continue    

    # After all queens have been checked, the score is returned.
    return score

# choose_next() selects the next best state from the list of successors and the given state.
# The original state is added to the list so that None can be returned if a local minimum is 
# reached.
def choose_next(curr, boulderX, boulderY):
    # possibleSucc is the list of successors along with the original state.
    possibleSucc = succ(curr, boulderX, boulderY)
    possibleSucc.append(curr)

    # The states in possibleSucc are added to the 2D array scoredList where the inner array
    # is a state's score followed by the state itself.
    scoredList = []
    for aState in possibleSucc:
        scoredList.append([f(aState, boulderX, boulderY), aState])

    # scoredList is sorted and the top score is taken from the item on top.
    list.sort(scoredList)
    topScore = scoredList[0][0]

    # Any states with a score equal to topScore are added to scoredSublist.
    scoredSublist = []
    for state in scoredList:
        if state[0] == topScore:
            scoredSublist.append(state[1])
        else:
            break

    # scoredSublist is sorted and the state on top is chosen. If this state differs
    # from the original, then it is returned. Otherwise, None is returned.
    list.sort(scoredSublist)
    if curr == scoredSublist[0]:
        return None
    else:
        return scoredSublist[0]

# nqueens() combines the above functions to find a local minimum or solution from the 
# state and boulder location given to it.
def nqueens(initial_state, boulderX, boulderY):
    nextState = initial_state
    previousState = None

    # This loop runs until a local minimum or solution is found. It keeps on generating better states
    # and putting them into nextState. If nextState ends up with a solution, it is printed and returned.
    # If nextState ends up with None (we reached a local minimum), previousState is returned. previousState
    # always holds the state that precedes nextState.
    while True:
        print(str(nextState) + " - f=" + str(f(nextState, boulderX, boulderY)))
        previousState = nextState
        nextState = choose_next(nextState, boulderX, boulderY)
        if nextState == None:
            return previousState
        elif f(nextState, boulderX, boulderY) == 0:
            print(str(nextState) + " - f=" + str(f(nextState, boulderX, boulderY)))
            return nextState
        
# nqueens_restart() tries k times to find a solution to placing n queens on an n*n board
# with a boulder at [boulderX, boulderY]. Starting states are generated randomly. If a 
# solution is found before it completes, the function returns and the solution is printed.
# If a solution is not found, the best local minimums that were found are printed. These
# minimums are also sorted when printed.
def nqueens_restart(n, k, boulderX, boulderY):
    # count is a counter variable to keep track of the amount of tries.
    count = 0
    # convergenceList is a 2D array of scores and the states that the scores
    # were derived from.
    convergenceList = []

    # This while loop tries to find a solution in the set amount of tries.
    while count < k:

        # randState is an array that holds a state of the board. It is generated randomly
        # and must be valid.
        randState = []
        for col in range(n):
            rand = random.randint(0, n-1)
            while col == boulderX and rand == boulderY:
                rand = random.randint(0, n-1)
            randState.append(rand)
        
        # randConvergence stores the solution or local minimum that is found for a given
        # starting state.
        randConvergence = nqueens(randState, boulderX, boulderY)
        print()

        # If a solution to the given state is found, the solution is printed and the
        # method returns immediately. Otherwise, the minimums that were found are added
        # to convergenceList.
        if f(randConvergence, boulderX, boulderY) == 0:
            print(randConvergence)
            return
        else:
            convergenceList.append([f(randConvergence, boulderX, boulderY), randConvergence])

        count += 1

    # convergenceList is sorted by scores to find the best states.
    list.sort(convergenceList)
    topScore = convergenceList[0][0]

    # States with the lowest scores are added to topConvergences. States with higher scores
    # are omitted.
    topConvergences = []
    for state in convergenceList:
        if state[0] == topScore:
            topConvergences.append(state[1])
        else:
            break

    # The states with the lowest scores are sorted and printed.
    list.sort(topConvergences)
    for state in topConvergences:
        print(str(state))
