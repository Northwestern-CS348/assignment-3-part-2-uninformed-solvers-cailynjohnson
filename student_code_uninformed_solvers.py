
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        # if current state of the node is the desired solution state, return true (we don't have to search for a solution)
        if self.currentState.state == self.victoryCondition:
            return True

        # otherwise go to the next unexplored state
        nextMoves = self.gm.getMovables()

        # assign variables to the current state and current depth of the node
        currState = self.currentState 
        currDepth = self.currentState.depth

        # if the current state is not a leaf node and has unexplored states
        if nextMoves != 0:
            
            # expand the node
            for currMove in nextMoves:

                self.gm.makeMove(currMove)

                nextState = GameState(self.gm.getGameState(), currDepth + 1, currMove)
                currState.children.append(nextState)

                nextState.parent = currState

                self.gm.reverseMove(currMove)

            # for each child of the current node, move to child if it's not been visited and change current state to child
            for currChild in currState.children:

                if currChild not in self.visited:

                    self.gm.makeMove(currChild.requiredMovable)
                    self.visited[currChild] = True

                    self.currentState = currChild

                    break

        # if the node doesn't have any more unexplored states, go back up the tree to continue searching 
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)

        # if the desired solution state is never reached, return false
        return False
        


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        
        return True
