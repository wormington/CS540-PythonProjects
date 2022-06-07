"""
    Author: Cade Wormington
    Class: CS 540
    Lecture: 
"""

import copy

# fill() takes the state given to it and fills the jug specified to its respective maximum.
# Note: fill() makes a copy of the state given to it; the original state is unaffected.
#
# state: the current state fill() should act on
# max: the state that holds the maximum capacity for each jug
# which: 0 or 1, specifies which of the two jugs to act on
def fill(state, max, which):
    # copies the current state and maxes out the respective jug
    newState = copy.deepcopy(state)
    newState[which] = max[which]
    return newState

# empty() takes the state given to it and empties the jug specified.
# Note: empty() makes a copy of the state given to it; the original state is unaffected.
#
# state: the current state empty() should act on
# max: the state that holds the maximum capacity for each jug
# which: 0 or 1, specifies which of the two jugs to act on
def empty(state, max, which):
    # copies the current state and empties the respective jug
    newState = copy.deepcopy(state)
    newState[which] = 0
    return newState

# xfer() takes the state given to it and transfers the contents of one jug to another. xfer() will
# not overfill jugs; if a jug does not have enough capacity for a transfer, only the remaining amount
# it can hold is transferred.
# Note: xfer() makes a copy of the state given to it; the original state is unaffected.
#
# state: the current state xfer() should act on
# max: the state that holds the maximum capacity for each jug
# source: 0 or 1, specifies which of the two jugs to pour
# dest: 0 or 1, specifies which of the two jugs to pour into
def xfer(state, max, source, dest):
    # copies the current state and determines how much available space is in the destination jug
    newState = copy.deepcopy(state)
    availableCap = max[dest] - state[dest]

    # if the source jug has less water than the amount the destination jug can take, the transfer
    # capacity is limited to that amount.
    if newState[source] < availableCap:
        availableCap = newState[source]

    # the same amount of water that is removed from the source is added to the destination
    newState[source] = state[source] - availableCap
    newState[dest] = state[dest] + availableCap
    return newState

# succ() lists all possible successor states that can be derived from the current state.
#
# state: the current state succ() should act on
# max: the state that holds the maximum capacity for each jug
def succ(state, max):
    stateList = []

    # if nothing happens, the same state can be a successor
    stateList.append(state)

    # if a jug has water, it can be emptied.
    if state[0] > 0:
        stateList.append(empty(state, max, 0))

        # if a jug has water and the opposite jug is not full, water can be transferred.
        if state[1] < max[1]:
            stateList.append(xfer(state, max, 0, 1))
    
    # if a jug is not full, it can be filled. 
    if state[0] < max[0]:
        stateList.append(fill(state, max, 0))

    # if a jug has water, it can be emptied.
    if state[1] > 0:
        stateList.append(empty(state, max, 1))

        # if a jug has water and the opposite jug is not full, water can be transferred.
        if state[0] < max[0]:
            stateList.append(xfer(state, max, 1, 0))

    # if a jug is not full, it can be filled.
    if state[1] < max[1]:
        stateList.append(fill(state, max, 1))
    
    # prints each available state on its own line
    for out in stateList:
        print(str(out))
