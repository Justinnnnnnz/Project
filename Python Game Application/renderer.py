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

This file contains the class that "renders" the image of our game.
"""
from typing import Dict, List, Tuple, Optional
import pygame

from actions import ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE,\
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, ACTION_KEY, ACTION_LABEL, COMBINE,\
    PAINT, PASS
from settings import BACKGROUND_COLOUR, TEXT_COLOUR, OUTLINE_THICKNESS, \
    OUTLINE_COLOUR, HIGHLIGHT_THICKNESS, HIGHLIGHT_COLOUR, COLOUR_LIST, \
    colour_name

Y_FONT_PADDING = 2


def _load_image(path_to_file: str) -> pygame.Surface:
    """
    Load an image from <path_to_file>.

    If an error occurs, print it before exiting the program.
    """
    try:
        image = pygame.image.load(path_to_file)
    except pygame.error as e:
        # Avoid outputting the stack trace, just show the error
        print('ERROR: ', e)
        raise SystemExit

    return image


def _print_to_image(text: str, x: int, y: int, font: pygame.font.Font,
                    image: pygame.Surface,
                    colour: Tuple[int, int, int] = TEXT_COLOUR) -> None:
    """Use <font> to print <text> to (<x>, <y>) on <image> with <colour>.
    """
    text_surface = font.render(text, 1, colour)
    image.blit(text_surface, (x, y))


def _print_human_instructions(x: int, y: int, text_height: int,
                              font: pygame.font.Font, image: pygame.Surface)\
        -> int:
    # Print a heading
    _print_to_image('Human Controls', x, y, font, image)

    # Indent the next items
    x += 10
    y += text_height + Y_FONT_PADDING

    text = 'Increase Level: S'
    _print_to_image(text, x, y, font, image)
    y += text_height + Y_FONT_PADDING
    text = 'Decrease Level: W'
    _print_to_image(text, x, y, font, image)
    y += text_height + Y_FONT_PADDING

    for action, key in ACTION_KEY.items():
        key_name = pygame.key.name(key).upper()
        label = ACTION_LABEL[action]
        text = f'{label}: {key_name}'

        _print_to_image(text, x, y, font, image)
        y += text_height + Y_FONT_PADDING

    return y


def _print_ai_instructions(x: int, y: int, text_height: int,
                           font: pygame.font.Font, image: pygame.Surface)\
        -> int:
    _print_to_image('Non-Human Controls', x, y, font, image)

    # Indent the next item
    x += 10
    y += text_height + Y_FONT_PADDING

    _print_to_image('Click Mouse to Continue', x, y, font, image)
    y += text_height + Y_FONT_PADDING

    return y


def _print_colours(x: int, y: int, text_height: int,
                   font: pygame.font.Font, image: pygame.Surface)\
        -> int:
    _print_to_image('Colours', x, y, font, image)

    # Indent the next item
    x += 10
    y += text_height + Y_FONT_PADDING

    for c in COLOUR_LIST:
        _print_to_image(colour_name(c), x, y, font, image, c)
        y += text_height + Y_FONT_PADDING

    return y


def _print_instructions(screen: pygame.Surface,
                        font: pygame.font.Font, height: int) -> \
        pygame.Surface:
    text_height = font.size("Test")[1]
    image = screen.subsurface(((750, 0), (250, height)))

    # Setup the initial position
    x_pos = 10
    y_pos = 5

    y_pos = _print_human_instructions(x_pos, y_pos, text_height, font, image)

    y_pos += text_height + Y_FONT_PADDING
    y_pos = _print_ai_instructions(x_pos, y_pos, text_height, font, image)

    y_pos += text_height + Y_FONT_PADDING
    _print_colours(x_pos, y_pos, text_height, font, image)

    return image


class Renderer:
    """
    A class designed to handle drawing the different aspects of a Blocky game.
    """
    # === Private Attributes ===
    # _screen:
    #   The pygame image to draw on for visualizing graphics.
    # _font:
    #   The font to use for text being drawn.
    # _images:
    #   A dictionary mapping actions to images that are displayed in the game.
    # _status_position:
    #   The (x, y) position of the status messages.
    _screen: pygame.Surface
    _instructions: pygame.Surface
    _images: Dict[Tuple[str, Optional[int]], pygame.Surface]
    _font: pygame.font.Font
    _status_position: Tuple[int, int]
    _clear_rect: Tuple[Tuple[int, int], Tuple[int, int]]

    def __init__(self, size: int) -> None:
        """Initialize this Renderer for a board with dimensions <size> x <size>.
        """
        self._font = pygame.font.Font(pygame.font.get_default_font(), 14)
        status_height = self._font.size("Player")[1]
        instructions_width = 250

        height = size + status_height + 2 * Y_FONT_PADDING
        width = size + instructions_width

        self._screen = pygame.display.set_mode((width, height))
        self._instructions = _print_instructions(self._screen, self._font,
                                                 height)

        self._status_position = (10, size + Y_FONT_PADDING)
        self._clear_rect = ((0, 0), (size, height))

        self._images = {
            ROTATE_CLOCKWISE: _load_image('images/rotate-cw.png'),
            ROTATE_COUNTER_CLOCKWISE: _load_image('images/rotate-ccw.png'),
            SWAP_HORIZONTAL: _load_image('images/swap-horizontal.png'),
            SWAP_VERTICAL: _load_image('images/swap-vertical.png'),
            SMASH: _load_image('images/smash.png'),
            COMBINE: _load_image('images/combine.png'),
            PAINT: _load_image('images/paint.png'),
            PASS: _load_image('images/pass.png')
        }

    def clear(self) -> None:
        """Clear the screen with BACKGROUND_COLOUR.
        """
        self._screen.fill(BACKGROUND_COLOUR, self._clear_rect)

    def draw_image(self, action: Tuple[str, Optional[int]],
                   pos: Tuple[int, int], size: int) -> None:
        """Draw the image that coincides with action at pos, stretched to fit
        size.

        If the action is not supported, no image is drawn.
        """
        if action in self._images:
            image = self._images[action]
            image = pygame.transform.scale(image, (size, size))
            self._screen.blit(image, pos)

    def draw_board(self, squares: List[Tuple[Tuple[int, int, int],
                                             Tuple[int, int], int]]) -> None:
        """Draw each block in blocks onto the screen.
        """
        for colour, pos, size in squares:
            rect = (pos[0], pos[1], size, size)
            pygame.draw.rect(self._screen, colour, rect, 0)
            pygame.draw.rect(self._screen, OUTLINE_COLOUR, rect,
                             OUTLINE_THICKNESS)

    def highlight_block(self, pos: Tuple[int, int], size: int) -> None:
        """Draw a highlighted square border at pos with size.
        """
        rect = (pos[0], pos[1], size, size)
        pygame.draw.rect(self._screen, HIGHLIGHT_COLOUR, rect,
                         HIGHLIGHT_THICKNESS)

    def text_height(self) -> int:
        """Return the height between lines of text in pixels.
        """
        return self._font.size("Test")[1] + Y_FONT_PADDING

    def print(self, text: str, x: int, y: int) -> None:
        """Print <text> to the (<x>, <y>) location on the screen.
        """
        _print_to_image(text, x, y, self._font, self._screen)

    def draw_status(self, message: str) -> None:
        """Draw the current status of the game.
        """
        surface = self._font.render(message, 1, TEXT_COLOUR)
        self._screen.blit(surface, self._status_position)

    def save_to_file(self, filename: str) -> None:
        """Save the current graphics on the screen to a file named <filename>.
        """
        pygame.image.save(self._screen, filename)
