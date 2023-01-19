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
Misha Schwartz, and Jaisie Sin.

=== Module Description ===

This file contains the global settings for the blocky game.
"""
from typing import Tuple

# Colours that we could use in the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PACIFIC_POINT = (1, 128, 181)
OLD_OLIVE = (138, 151, 71)
REAL_RED = (199, 44, 58)
MELON_MAMBO = (234, 62, 112)
DAFFODIL_DELIGHT = (255, 211, 92)
TEMPTING_TURQUOISE = (75, 196, 213)

# A pallette of the colours we use in the game
COLOUR_LIST = [PACIFIC_POINT, REAL_RED, OLD_OLIVE, DAFFODIL_DELIGHT]

# The game board will be a square with this size.
BOARD_SIZE = 750

# The background will be this colour.
BACKGROUND_COLOUR = BLACK
# Text will have this colour.
TEXT_COLOUR = WHITE
# Blocks will have this colour outline.
OUTLINE_COLOUR = BLACK
# Blocks will have this thick of an outline.
OUTLINE_THICKNESS = 3
# Blocks will be highlighted with this colour.
HIGHLIGHT_COLOUR = TEMPTING_TURQUOISE
# Highlighted blocks will have this thickness to the highlight.
HIGHLIGHT_THICKNESS = 5

# The number of seconds a move is animated for.
ANIMATION_DURATION = 1


def colour_name(colour: Tuple[int, int, int]) -> str:
    """Return the colour name associated with this colour value, or the empty
    string if this colour value isn't in our colour list.

    >>> colour_name((1, 128, 181))
    'Pacific Point'
    >>> colour_name(PACIFIC_POINT)
    'Pacific Point'
    """
    colour_names = {
        PACIFIC_POINT: 'Pacific Point',
        REAL_RED: 'Real Red',
        OLD_OLIVE: 'Old Olive',
        DAFFODIL_DELIGHT: 'Daffodil Delight'
    }

    if colour in colour_names:
        return colour_names[colour]
    else:
        return ''
