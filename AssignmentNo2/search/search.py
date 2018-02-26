# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import Stack
from util import Queue
from util import PriorityQueue

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    dfsStack = Stack()
    dfsClosed = dict()
    # object the holds node properties
    activeNode = {'nodeAction': None, 'nodeState': startState, 'nodeParent': None}

    dfsStack.push(activeNode)
    while True:
        if dfsStack.isEmpty():
            break
        activeNode = dfsStack.pop()
        state = activeNode["nodeState"]
        if dfsClosed.has_key((state)):
            continue
        else:
            dfsClosed[state] = True
        if problem.isGoalState(state) == True:
            break
        for expandedNodes in problem.getSuccessors(state):
            if not dfsClosed.has_key((expandedNodes[0])):
                # push the child node with child node properties, important to save the parent path ("nodeParent")
                dfsStack.push({'nodeAction': expandedNodes[1], 'nodeState': expandedNodes[0], 'nodeParent': activeNode})
    actions = []
    while True:
        if activeNode["nodeAction"] == None:
            break
        actions.insert(0, activeNode["nodeAction"])
        activeNode = activeNode["nodeParent"]
    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    bfsStack = Queue()
    bfsClosed = dict()
    # object the holds node properties
    activeNode = {'nodeAction': None, 'nodeState': startState, 'nodeParent': None}

    bfsStack.push(activeNode)
    while True:
        if bfsStack.isEmpty():
            break
        activeNode = bfsStack.pop()
        state = activeNode["nodeState"]
        if bfsClosed.has_key((state)):
            continue
        else:
            bfsClosed[state] = True
        if problem.isGoalState(state) == True:
            break
        for expandedNodes in problem.getSuccessors(state):
            if not bfsClosed.has_key((expandedNodes[0])):
                # push the child node with child node properties, important to save the parent path ("nodeParent")
                bfsStack.push({'nodeAction': expandedNodes[1], 'nodeState': expandedNodes[0], 'nodeParent': activeNode})
    actions = []
    while True:
        if activeNode["nodeAction"] == None:
            break
        actions.insert(0, activeNode["nodeAction"])
        activeNode = activeNode["nodeParent"]
    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    ucsStack = PriorityQueue()
    ucsClosed = dict()
    # object the holds node properties
    activeNode = {'nodeAction': None, 'nodeState': startState, 'nodeParent': None, 'nodeCost': 0}
    ucsStack.push(activeNode, 0)
    while True:
        if ucsStack.isEmpty():
            break
        else:
            activeNode = ucsStack.pop()
        state = activeNode["nodeState"]
        cost = activeNode["nodeCost"]
        if ucsClosed.has_key((state)):
            continue
        ucsClosed[state] = True
        if problem.isGoalState(state) == True:
            break
        for expandedNodes in problem.getSuccessors(state):
            if not ucsClosed.has_key((expandedNodes[0])):
                totalCost = expandedNodes[2] + cost
                # push the child node with child node properties, important to save the parent path ("nodeParnt") and cost of the node
                ucsStack.push({'nodeAction': expandedNodes[1], 'nodeState': expandedNodes[0], 'nodeParent': activeNode,
                               'nodeCost': totalCost}, totalCost)
    actions = []
    while True:
        if activeNode["nodeAction"] == None:
            break
        actions.insert(0, activeNode["nodeAction"])
        activeNode = activeNode["nodeParent"]
    return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    ucsStack = PriorityQueue()
    ucsClosed = dict()
    # object the holds node properties
    activeNode = {'nodeAction': None, 'nodeState': startState, 'nodeParent': None, 'nodeCost': 0}
    heuristicVal = heuristic(startState, problem)
    totalCombinedCost = 0 + heuristicVal
    ucsStack.push(activeNode, totalCombinedCost)
    while True:
        if ucsStack.isEmpty():
            break
        activeNode = ucsStack.pop()
        state = activeNode["nodeState"]
        cost = activeNode["nodeCost"]
        if ucsClosed.has_key((state)):
            continue
        else:
            ucsClosed[state] = True
        if problem.isGoalState(state) == True:
            break
        for expandedNodes in problem.getSuccessors(state):
            if not ucsClosed.has_key((expandedNodes[0])):
                totalCost = expandedNodes[2] + cost
                totalCombinedCost = totalCost + heuristic(expandedNodes[0], problem)
                # push the child node with child node properties, important to save the parent path ("nodeParnt") and cost and heuristic cost of the node
                ucsStack.push({'nodeAction': expandedNodes[1], 'nodeState': expandedNodes[0], 'nodeParent': activeNode,
                               'nodeCost': totalCost}, totalCombinedCost)
    actions = []
    while True:
        if activeNode["nodeAction"] == None:
            break
        actions.insert(0, activeNode["nodeAction"])
        activeNode = activeNode["nodeParent"]
    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
