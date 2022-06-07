"""
    Author: Cade Wormington
    Class: CS 540
    Lecture: 
"""

import random
import copy

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
            
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        # Generates a list of successors and scores them. The scores are a sum of the heuristic value of the successor
        # and the minimax value of its future states. Chooses the next move with the highest score.
        succList = self.succ(state)
        scoredSuccs = []
        for succ in succList:
            scoredSuccs.append([self.Max_Value(succ, 2, 0) + self.heuristic_game_value(succ), succ])
        scoredSuccs.sort(reverse = True)
        nextMove = scoredSuccs[0][1]

        # TODO: detect drop phase
        # Counts all of the pieces on the board to determine if we are in drop phase.
        drop_phase = False
        count = 0
        for row in range(5):
            for col in range(5):
                if (state[row][col] == 'r' or state[row][col] == 'b'):
                    count += 1
        if count < 8:
            drop_phase = True   
        
        move = []
        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            
            # These for loops look at the game board and find differences between the current state
            # and the next state. It finds which piece was moved where and sets the source tuple/destination tuple
            # accordingly.
            source = None
            moveTo = None
            for row in range(5):
                for col in range(5):
                    if state[row][col] == nextMove[row][col]:
                        pass
                    else:
                        if nextMove[row][col] == ' ':
                            source = (row, col)
                        else:
                            moveTo = (row, col)
            
            move = [moveTo, source]
        else:
            # select an unoccupied space randomly
            # TODO: implement a minimax algorithm to play better
            
            # These for loops find the difference between the next move and current state
            # and set the move variable accordingly.
            for row in range(5):
                for col in range(5):
                    if state[row][col] == nextMove[row][col]:
                        pass
                    else:
                        move = [(row, col)]

        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)
        
    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
                
                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece
        
    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
        
    def game_value(self, state):
        """ Checks the current board status for a win condition
        
        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 2x2 box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        if state[0][0] != ' ' and state[0][0] == state[1][1] == state[2][2] == state[3][3]:
                    return 1 if state[0][0]==self.my_piece else -1
                    
        if state[1][1] != ' ' and state[1][1] == state[2][2] == state[3][3] == state[4][4]:
                    return 1 if state[1][1]==self.my_piece else -1
        
        if state[0][1] != ' ' and state[0][1] == state[1][2] == state[2][3] == state[3][4]:
                    return 1 if state[0][1]==self.my_piece else -1
        
        if state[1][0] != ' ' and state[1][0] == state[2][1] == state[3][2] == state[4][3]:
                    return 1 if state[1][0]==self.my_piece else -1

        # TODO: check / diagonal wins
        if state[4][0] != ' ' and state[4][0] == state[3][1] == state[2][2] == state[1][3]:
                    return 1 if state[4][0]==self.my_piece else -1
        
        if state[3][1] != ' ' and state[3][1] == state[2][2] == state[1][3] == state[0][4]:
                    return 1 if state[3][1]==self.my_piece else -1
        
        if state[3][0] != ' ' and state[3][0] == state[2][1] == state[1][2] == state[0][3]:
                    return 1 if state[3][0]==self.my_piece else -1
        
        if state[4][1] != ' ' and state[4][1] == state[3][2] == state[2][3] == state[1][4]:
                    return 1 if state[4][1]==self.my_piece else -1
        
        # TODO: check 2x2 box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col] == state[row][col+1] == state[row+1][col+1]:
                    return 1 if state[row][col] == self.my_piece else -1
        
        return 0 # no winner yet

    # Generates a list of valid successor states from a given state for our AI.
    def succ(self, state):

        # Checks to see if we are in drop phase.
        drop_phase = False
        count = 0
        for row in range(5):
            for col in range(5):
                if (state[row][col] == 'r' or state[row][col] == 'b'):
                    count += 1
        if count < 8:
            drop_phase = True

        succList = []
        # If we are in drop phase, the successors are made by placing one of our pieces into any empty space.
        if drop_phase:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        newState = copy.deepcopy(state)
                        newState[row][col] = self.my_piece
                        succList.append(newState)
        # If we are not in drop phase, the successors are made by moving all of our pieces into any adjacent empty space.
        else:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == self.my_piece:
                        newState = copy.deepcopy(state)
                        for newRow in range(-1, 1, 1):
                            for newCol in range(-1, 1, 1):
                                if (row + newRow < 5 and row + newRow > -1 and col + newCol < 5 and col + newCol > -1):
                                    if (newState[row + newRow][col + newCol] == ' '):
                                        newState[row + newRow][col + newCol] = self.my_piece
                                        newState[row][col] = ' '
                                        succList.append(newState)

        return succList

    # Generates a list of valid successor states from a given state for the other player.
    def succOther(self, state):

        # Checks to see if we are in drop phase.
        drop_phase = False
        count = 0
        for row in range(5):
            for col in range(5):
                if (state[row][col] == 'r' or state[row][col] == 'b'):
                    count += 1
        if count < 8:
            drop_phase = True

        theirPiece = 'r'
        if self.my_piece == 'r':
            theirPiece = 'b'

        succList = []
        # If we are in drop phase, the successors are made by placing one of their pieces into any empty space.
        if drop_phase:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        newState = copy.deepcopy(state)
                        newState[row][col] = theirPiece
                        succList.append(newState)
        # If we are not in drop phase, the successors are made by moving all of their pieces into any adjacent empty space.
        else:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == theirPiece:
                        newState = copy.deepcopy(state)
                        for newRow in range(-1, 1, 1):
                            for newCol in range(-1, 1, 1):
                                if (row + newRow < 5 and row + newRow > -1 and col + newCol < 5 and col + newCol > -1):
                                    if (newState[row + newRow][col + newCol] == ' '):
                                        newState[row + newRow][col + newCol] = theirPiece
                                        newState[row][col] = ' '
                                        succList.append(newState)

        return succList

    # A heuristic for the AI player. Takes into account how many pieces are close to the center of the board and how many pieces are adjacent to eachother.
    def heuristic_game_value(self, state):
        # Scores for each space. The closer to the middle, the higher the score.
        spaceScores = [[0, 0, 0, 0, 0], [0, 0.01, 0.01, 0.01, 0], [0, 0.01, 0.02, 0.01, 0], [0, 0.01, 0.01, 0.01, 0], [0, 0, 0, 0, 0]]

        # Uses game_value to check for a winning state.
        stateVal = self.game_value(state)
        if stateVal != 0:
            return stateVal
        # If no winning state, calculates the heuristic.
        else:
            # TODO
            myScore = 0
            myFCount = 0
            for row in range(5):
                for col in range(5):
                    if state[row][col] == self.my_piece:
                        # Adds to the score based on where pieces are located.
                        myScore += spaceScores[row][col]

                        # Checks to see if a piece has more friendly pieces adjacent to it.
                        byFriendly = False
                        for adjRow in range(-1, 1, 1):
                            for adjCol in range(-1, 1, 1):
                                if (row + adjRow < 5 and row + adjRow > -1 and col + adjCol < 5 and col + adjCol > -1):
                                    if state[row + adjRow][col + adjCol] == self.my_piece:
                                        byFriendly = True
                        if byFriendly:
                            myFCount += 1

            # The more pieces with an adjacent piece, the higher the score bonus.
            myAdjacency = 0
            if myFCount == 2:
                myAdjacency = 0.2
            elif myFCount == 3:
                myAdjacency = 0.5
            elif myFCount == 4:
                myAdjacency = 0.9

            myScore = myScore + myAdjacency
        return myScore

    # A heuristic for the other player. Takes into account how many pieces are close to the center of the board and how many pieces are adjacent to eachother.
    def heuristic_game_value_other(self, state):
        # Scores for each space. The closer to the middle, the higher the score.
        spaceScores = [[0, 0, 0, 0, 0], [0, 0.01, 0.01, 0.01, 0], [0, 0.01, 0.02, 0.01, 0], [0, 0.01, 0.01, 0.01, 0], [0, 0, 0, 0, 0]]

        theirPiece = 'r'
        if self.my_piece == 'r':
            theirPiece = 'b'

        # Uses game_value to check for a winning state.
        stateVal = self.game_value(state)
        if stateVal != 0:
            return stateVal
        # If no winning state, calculates the heuristic.
        else:
            # TODO
            myScore = 0
            myFCount = 0
            for row in range(5):
                for col in range(5):
                    if state[row][col] == theirPiece:
                        # Adds to the score based on where pieces are located.
                        myScore += spaceScores[row][col]

                        # Checks to see if a piece has more friendly pieces adjacent to it.
                        byFriendly = False
                        for adjRow in range(-1, 1, 1):
                            for adjCol in range(-1, 1, 1):
                                if (row + adjRow < 5 and row + adjRow > -1 and col + adjCol < 5 and col + adjCol > -1):
                                    if state[row + adjRow][col + adjCol] == theirPiece:
                                        byFriendly = True
                        if byFriendly:
                            myFCount += 1

            # The more pieces with an adjacent piece, the higher the score bonus.
            myAdjacency = 0
            if myFCount == 2:
                myAdjacency = 0.2
            elif myFCount == 3:
                myAdjacency = 0.5
            elif myFCount == 4:
                myAdjacency = 0.9

            myScore = myScore + myAdjacency
        return myScore

    # The max_value portion of the minimax algorithm.
    def Max_Value(self, state, depth, count):
        stateVal = self.game_value(state)
        if (stateVal != 0 or count >= depth):
            if (stateVal == 0):
                return self.heuristic_game_value(state)
            else:
                return stateVal
        else:
            a = float('-inf')
            succList = self.succ(state)
            for aState in succList:
                a = max(a, self.Min_Value(aState, depth, count+1))

            return a

    # The min_value portion of the minimax algorithm.
    def Min_Value(self, state, depth, count):
        stateVal = self.game_value(state)
        if (stateVal != 0 or count >= depth):
            if (stateVal == 0):
                return (-1 * self.heuristic_game_value_other(state))
            else:
                return stateVal
        else:
            b = float('inf')
            succList = self.succOther(state)
            for aState in succList:
                b = min(b, self.Max_Value(aState, depth, count+1))

            return b
