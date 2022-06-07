"""
    Author: Cade Wormington
    Class: CS 540
    Lecture: 
"""

import random as rand

# pick_envelope() simulates the Monty Hall problem using the random module.
# switch is a boolean value that determines if the envelopes should be switched
# after a ball is drawn.
# verbose determines whether or not the function should print the details of each simulation.
def pick_envelope(switch, verbose):
    # Creates envelopes as empty arrays.
    envelope0 = []
    envelope1 = []

    # Randomly selects where red ball will be. 1 and 2 correspond to envelope1.
    # 3 and 4 correspond to envelope2. All positions that are not selected as the red
    # ball will contain black balls.
    red = rand.randint(0, 3)

    # Places the balls in their envelopes.
    for num in range(4):
        if num < 2:
            if num == red:
                envelope0.append("r")
            else:
                envelope0.append("b")
        else:
            if num == red:
                envelope1.append("r")
            else:
                envelope1.append("b")

    # Prints the contents of the envelopes if verbose is True.
    if verbose:
        print("Envelope 0: " + str(envelope0[0]) + " " + str(envelope0[1]))
        print("Envelope 1: " + str(envelope1[0]) + " " + str(envelope1[1]))

    # Randomly selects an envelope and a ball in the envelope.
    pickEnvelope = rand.randint(0, 1)
    pickBall = rand.randint(0, 1)
    
    # If pickEnvelope checks to see which envelope was picked. If envelope1 was picked,
    # the if-half of this if/else runs.
    if pickEnvelope:
        # Gets the string of the chosen ball in the chosen envelope.
        ball = envelope1[pickBall]

        # Prints which envelope is chosen and which ball is chosen if verbose is True.
        if verbose:
            print("I picked envelope 1")
            print("and drew a " + ball)

        # If the chosen ball is the red, we immediately return True because we picked
        # correctly. 
        # If we did not choose the red ball, we check to see if switch is True. If so, 
        # we return True if the ball is in envelope 0, and we return False if it is not.
        # If switch is False, we check the other ball in this envelope to see if it is red
        # and return whether or not we chose correctly.
        if (ball == "r"):
            return True   
        else:
            if switch:
                if verbose:
                    print("Switch to envelope 0")

                return ("r" in envelope0)
            else:
                return ("r" in envelope1)
    # Runs if envelope 0 was picked.
    else:
        # Gets the string of the chosen ball in the chosen envelope.
        ball = envelope0[pickBall]

        # Prints which envelope is chosen and which ball is chosen if verbose is True.
        if verbose:
            print("I picked envelope 0")
            print("and drew a " + ball)

        # If the chosen ball is the red, we immediately return True because we picked
        # correctly. 
        # If we did not choose the red ball, we check to see if switch is True. If so, 
        # we return True if the ball is in envelope 1, and we return False if it is not.
        # If switch is False, we check the other ball in this envelope to see if it is red
        # and return whether or not we chose correctly.
        if (ball == "r"):
            return True
        else:
            if switch:
                if verbose:
                    print("Switch to envelope 1")

                return ("r" in envelope1)
            else:
                return ("r" in envelope0)

# run_simulation() uses pick_envelope() to simulate the Monty Hall problem multiple times.
# The amount of times the simulation chose correctly is printed at the end.
#  
# n is the amount of simulations to run. The simulation is run n times with switching
# and n times without switching.         
def run_simulation(n):
    # switchCount keeps track of the amount of successful runs while switching.
    switchCount = 0
    
    # The first for loop runs the simulation with switching n times.
    for a in range(n):
        if pick_envelope(True, False):
            switchCount += 1

    # The second for loop runs the simulation without switching n times.
    noSwitchCount = 0
    for b in range(n):
        if pick_envelope(False, False):
            noSwitchCount += 1

    # Prints the amount of succesful runs while switching and while not switching.
    print("After " + str(n) + " simulations: ")
    print("  Switch successful: " + "{:.2%}".format(switchCount/n))
    print("  No-switch successful: " + "{:.2%}".format(noSwitchCount/n))
