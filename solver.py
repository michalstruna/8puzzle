#!/usr/bin/python3

import numpy
from queue import PriorityQueue

class Array:

    @staticmethod
    def find(array, item):
        position = numpy.where(array == item)

        if len(position[0]) > 0 and len(position[1]) > 0:
            return (position[0][0], position[1][0])

class Path:

    @staticmethod
    def get_action_cost(action):
        return abs(action[0]) + 3 * action[1]

    @staticmethod
    def get_cost(path):
        cost = 0

        for action in path:
            cost += Path.get_action_cost(action)

        return cost

class State:

    @staticmethod
    def create(area, field, rotation = 0):
        pos = Array.find(area, field)

        if pos:
            return (pos[0], pos[1], rotation)

    @staticmethod
    def equals(state1, state2, only_position = False):
        return state1[0] == state2[0] and state1[1] == state2[1] and (only_position or state1[2] == state2[2])

    @staticmethod
    def to_string(state):
        return ",".join(map(str, state))

    @staticmethod
    def is_allowed(area, state):
        return 0 <= state[0] < area.shape[0] and 0 <= state[1] < area.shape[1] and area[(state[0], state[1])] != 1

    @staticmethod
    def apply_action(area, state, action):
        newState = [state[0], state[1], state[2]]

        if action[0] != 0:
            newState[2] = ((newState[2] + action[0] + 4) % 4)
        else:
            if newState[2] == 0:
                newState[0] -= action[1]
            elif newState[2] == 1:
                newState[1] += action[1]
            elif newState[2] == 2:
                newState[0] += action[1]
            elif newState[2] == 3:
                newState[1] -= action[1]

        return newState

class Node:

    ID = 0
    STATE = 1
    PARENT = 2
    ACTION = 3
    PATH_EVAL = 4
    PATH_COST = 5

    count = 0

    @staticmethod
    def create(state, goal, parent = None, action = None):
        id = State.to_string(state)
        path_eval = (abs(goal[0] - state[0]) + abs(goal[1] - state[1])) ** 2
        path_cost = 0

        path_eval *= path_eval

        if parent:
            path_cost = parent[Node.PATH_COST] + Path.get_action_cost(action)
        
        return (id, state, parent, action, path_eval, path_cost)

    @staticmethod
    def add(node, queue):
        queue.put((node[Node.PATH_COST] + node[Node.PATH_EVAL], node))

    @staticmethod
    def get(queue):
        return queue.get()[1]

    @staticmethod
    def get_successors(node, goal, area, explored):
        for change in ((-1, 0), (1, 0), (2, 0), (0, 1)):
            newState = State.apply_action(area, node[Node.STATE], change)

            if State.is_allowed(area, newState):
                successor = Node.create(newState, goal, node, change)

                if (successor[Node.ID] not in explored):
                    yield successor

    @staticmethod
    def get_path(node):
        actions = []
        current = node

        while current[Node.ACTION] != None:
            actions.insert(0, current[Node.ACTION])
            current = current[Node.PARENT]

        return actions


class PathFinder:

    def get_expanded_states_count(self):
        return len(self.explored)

    def find_path(self, area):
        self.explored = set()
        self.fringe = PriorityQueue()
        init = State.create(area, 2)
        goal = State.create(area, 3)

        if not init or not goal:
            return None

        if State.equals(init, goal):
            return []

        Node.add(Node.create(init, goal), self.fringe)

        while not self.fringe.empty():
            node = Node.get(self.fringe)

            self.explored.add(node[Node.ID])

            for successor in Node.get_successors(node, goal, area, self.explored):
                if State.equals(successor[Node.STATE], goal, True):
                    return Node.get_path(successor)

                Node.add(successor, self.fringe)