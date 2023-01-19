"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import random
from typing import List, Tuple
from block import Block
from settings import COLOUR_LIST


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    # TODO: Implement Me
    goals = []
    goal_class = random.choice([PerimeterGoal, BlobGoal])
    random_colours = []
    for _ in range(num_goals):
        random_colours.append(random.choice(COLOUR_LIST))
    for sub in range(num_goals):
        goals.append(goal_class(random_colours[sub]))
    return goals  # FIXME


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    # TODO: Implement me

    n = pow(2, block.max_depth - block.level)
    if block.level == block.max_depth:
        return [[block.colour]]
    elif block.level < block.max_depth and len(block.children) == 0:
        return [[block.colour] * n] * n
    elif block.level == block.max_depth - 1 and len(block.children) != 0:
        return [[block.children[1].colour, block.children[2].colour],
                [block.children[0].colour, block.children[3].colour]]
    else:
        temp = []
        for i in [block.children[1],
                  block.children[2], block.children[0], block.children[3]]:
            temp.append(_flatten(i))

        l01 = [y for x in zip(temp[0], temp[1]) for y in x]
        temp[0], temp[1] = l01[:len(l01) // 2], l01[len(l01) // 2:]

        l23 = [a for b in zip(temp[2], temp[3]) for a in b]
        temp[2], temp[3] = l23[:len(l23) // 2], l23[len(l23) // 2:]

        res = []

        for first in temp:
            for second in range(0, len(first), 2):
                res.append(first[second]+first[second+1])
        return res


def neighbors(position: Tuple[int, int],
              board: List[List[Tuple[int, int, int]]]) -> List[Tuple[int, int]]:
    """Returns a list of position of neighbors of blob self.

    Precondition: board is flattened"""
    max_row = len(board) - 1
    max_column = len(board[0]) - 1
    l = []

    # left
    if position[0] >= 1:
        l.append((position[0] - 1, position[1]))

    # right
    if position[0] <= max_row - 1:
        l.append((position[0] + 1, position[1]))

    # top
    if position[1] >= 1:
        l.append((position[0], position[1] - 1))

    # bottom
    if position[1] <= max_column - 1:
        l.append((position[0], position[1] + 1))
    return l


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """A player goal in the game of Blocky.

        This is an abstract class. Only child classes should be instantiated.

        === Attributes ===
        colour:
            The target colour for this goal, that is the colour to which
            this goal applies.
        """
    def score(self, board: Block) -> int:
        # TODO: Implement me
        flatten_board = _flatten(board)
        size = len(flatten_board)
        perimeter = []
        # add the first column
        for i in flatten_board[0]:
            perimeter.append(i)
        # add the top and bottom
        for i in range(size):
            perimeter.append(flatten_board[i][0])
            perimeter.append(flatten_board[i][size - 1])
        # add the last column
        for i in flatten_board[-1]:
            perimeter.append(i)
        return sum(map(lambda x: x == self.colour, perimeter))

    def description(self) -> str:
        # TODO: Implement me
        return 'Perimeter'  # FIXME


class BlobGoal(Goal):
    """A player goal in the game of Blocky.

        This is an abstract class. Only child classes should be instantiated.

        === Attributes ===
        colour:
            The target colour for this goal, that is the colour to which
            this goal applies.
        """
    def score(self, board: Block) -> int:
        # TODO: Implement me
        score = [0]
        flatten_board = _flatten(board)
        for col in range(len(flatten_board)):
            for row in range(len(flatten_board[col])):
                if flatten_board[col][row] == self.colour:
                    score.append(self._undiscovered_blob_size((col,
                                                               row),
                                                              flatten_board,
                                                              []))
        return max(score)

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        # TODO: Implement me
        # if pos is out of bounds for board
        if pos[0] > len(board) - 1 or pos[1] > len(board[0]) - 1:
            return 0

        # initialize the "visited" list
        if len(visited) == 0:
            for i in range(len(board)):
                visited.append([])
                for _ in range(len(board[i])):
                    visited[i].append(-1)
        # if not visited
        score = 0
        lst = []
        if visited[pos[0]][pos[1]] == \
                -1 and board[pos[0]][pos[1]] == self.colour:
            score += 1
            visited[pos[0]][pos[1]] = 1
            # now check the neighbors
            for neighbor in neighbors(pos, board):
                # if there is a neighbor that is not visited, recurse
                if visited[neighbor[0]][neighbor[1]] == -1:
                    lst.append(self._undiscovered_blob_size(neighbor,
                                                            board,
                                                            visited))

                # if it is not the same colour, update visited.
            else:
                visited[pos[0]][pos[1]] = 0

        return score + sum(lst)

    def description(self) -> str:
        # TODO: Implement me
        return 'Your aim is to maximized the connected area of blocks ' \
               'of a given colour. Two blocks are connected if their sides ' \
               'touch; touching corners does not count. Th score would count ' \
               'as the unit cells in the largest blob of the given colour.'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
