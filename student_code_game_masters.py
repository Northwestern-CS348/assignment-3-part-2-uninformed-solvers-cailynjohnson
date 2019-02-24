from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """

        # create inner tuples for each peg
        peg1Tuple = tuple()
        peg2Tuple = tuple()
        peg3Tuple = tuple()

        # begin by checking the smallest disk
        currDisk = 1

        while (True):

            diskFound = False

            # check every fact in the knowledge base
            for currFact in self.kb.facts:
                
                # if the fact indicates a disk is on a peg
                if currFact.statement.predicate == "on":
                    
                    # get the disk and peg numbers
                    disk = currFact.statement.terms[0].term.element
                    peg = currFact.statement.terms[1].term.element
                    diskInt = int(disk[-1])
                    pegInt = int(peg[-1])

                    # if the disk number is the disk we're checking
                    if diskInt == currDisk:

                        diskFound = True
                        
                        # add tuple of disk number to corresponding peg number tuple
                        if pegInt == 1:
                            peg1Tuple += tuple([diskInt])
                        elif pegInt == 2:
                            peg2Tuple += tuple([diskInt])
                        elif pegInt == 3:
                            peg3Tuple += tuple([diskInt])

                        # check next largest disk
                        currDisk += 1
                        
                        break

            # if no other disks are found
            if diskFound == False:
                
                # return a tuple of tuples
                return (peg1Tuple, peg2Tuple, peg3Tuple)



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        # CREATION AND ASSIGNMENT
        # assigns variables to movable statement terms
        terms = movable_statement.terms
        movableDisk = str(terms[0])
        initialPeg = str(terms[1])
        targetPeg = str(terms[2])
        currState = self.getGameState()

        # creates empty lists for facts that must be retracted and asserted as a result of the move
        retractFacts = []
        assertFacts = []


        # INITIAL PEG CHANGES
        # retracts 'on' and 'top' initial peg facts
        retractFacts.append(parse_input("fact: (on " + movableDisk + " " + initialPeg + ")"))
        retractFacts.append(parse_input("fact: (top " + movableDisk + " " + initialPeg + ")"))

        initialPegTuple = currState[int(initialPeg[-1]) - 1]
        if len(initialPegTuple) > 1:
            assertFacts.append(parse_input("fact: top disk" + str(initialPegTuple[1]) + " " + initialPeg + ")"))
        else:
            assertFacts.append(parse_input("fact: (empty " + initialPeg + ")"))
        

        # TARGET PEG CHANGES
        # asserts 'on' and 'top' target peg facts 
        assertFacts.append(parse_input("fact: (on " + movableDisk + " " + targetPeg + ")"))
        assertFacts.append(parse_input("fact: (top " + movableDisk + " " + targetPeg + ")"))

        targetPegTuple = currState[int(targetPeg[-1]) - 1] 
        if len(targetPegTuple) == 0: 
            retractFacts.append(parse_input("fact: (empty " + targetPeg + ")"))
        else:
            retractFacts.append(parse_input("fact: top disk" + str(targetPegTuple[0]) + " " + targetPeg + ")"))


        # RETRACT AND ASSERT
        # retracts each fact that must be retracted from the KB as a result of the move
        for currFact in retractFacts:
            self.kb.kb_retract(currFact)

        # asserts each fact that must be asserted into the KB as a result of the move
        for currFact in assertFacts:
            self.kb.kb_assert(currFact)
        



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """

        # create inner tuples for each row
        row1Tuple = tuple()
        row2Tuple = tuple()
        row3Tuple = tuple()

        # for rows 1, 2, and 3
        for currRow in range(1,4): 

            # for columns 1, 2, and 3
            for currColumn in range(1,4):

                tileFound = False

                # check every fact in the knowledge base
                for currFact in self.kb.facts:

                    # if the fact indicates the position of a tile
                    if currFact.statement.predicate == "posn":

                        # get the tile, column, and row terms 
                        tile = currFact.statement.terms[0].term.element
                        column = currFact.statement.terms[1].term.element
                        row = currFact.statement.terms[2].term.element

                        # if the tile is not empty, get the tile, column, and row numbers
                        if tile != "empty":
                            tileInt = int(tile[-1])
                            columnInt = int(column[-1])
                            rowInt = int(row[-1])

                        # else the tile must be empty, so assign its tile number to -1 and get the column and row numbers
                        else:
                            tileInt = -1
                            columnInt = int(column[-1])
                            rowInt = int(row[-1])

                        # if the column number and row number we're checking is the column and row we're checking
                        if columnInt == currColumn and rowInt == currRow:

                            tileFound = True

                            # add tuple of tile number to corresponding row number tuple
                            if rowInt == 1:
                                row1Tuple += tuple([tileInt])
                            elif rowInt == 2:
                                row2Tuple += tuple([tileInt])
                            elif rowInt == 3:
                                row3Tuple += tuple([tileInt])

                            break

                if tileFound == False:

                    if currRow == 1:
                        row1Tuple += tuple([-1])
                    elif currRow == 2:
                        row2Tuple += tuple([-1])
                    elif currRow == 3:
                        row3Tuple += tuple([-1])

        # return a tuple of tuples 
        return (row1Tuple, row2Tuple, row3Tuple)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        # CREATION AND ASSIGNMENT
        # assigns variables to movable statement terms
        terms = movable_statement.terms
        movableTile = terms[0].term.element
        initialX = terms[1].term.element
        initialY = terms[2].term.element
        targetX = terms[3].term.element
        targetY = terms[4].term.element

        # creates empty lists for facts that must be retracted and asserted as a result of the move
        retractFacts = []
        assertFacts = []


        # INITIAL PEG CHANGES
        # retracts facts with old positions for moved tile and empty tile
        assertFacts.append(parse_input("fact: (posn  empty " + initialX + " " + initialY + ")"))
        retractFacts.append(parse_input("fact: (posn " + movableTile + " " + initialX + " " + initialY + ")"))


        # TARGET PEG CHANGES
        # asserts facts with new positions for moved tile and empty tile
        retractFacts.append(parse_input("fact: (posn  empty " + targetX + " " + targetY + ")"))
        assertFacts.append(parse_input("fact: (posn " + movableTile + " " + targetX + " " + targetY + ")"))


        # RETRACTION AND ASSERTION
        # retracts each fact that must be retracted from the KB as a result of the move
        for currFact in retractFacts:
            self.kb.kb_retract(currFact)

        # asserts each fact that must be asserted into the KB as a result of the move
        for currFact in assertFacts:
            self.kb.kb_assert(currFact)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
