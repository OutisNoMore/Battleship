"""All back-end utilities needed to play a game of Battleship

  Classes used include Window, Error, and Flag Enums
  The Window enum represents the different windows used during the game.
  The Error enum are the errors returned, and the Flags are the possible
  results of an attack.
"""
from enum import Enum

class Window(Enum):
    """Enum that represents different game windows

    Represents different game windows that are displayed
    during game play.
    """
    PLACE_SHIP = 0    # Window for placing ships
    PLAYER_TURN = 1   # Player's turn window
    COMPUTER_TURN = 2 # Window for the computer's turn
    GAME_OVER = 3     # Game over window


class Error(Enum):
    """Enum to represent Errors

    Represents different error states
    that can be returned.
    """
    NO_ERROR = 0      # No Error has occurred
    SHIP_EXISTS = 1   # Another ship already exists at coordinate
    DIAGONAL = 2      # Ships cannot be placed in diagonal cells
    SPREAD_APART = 3  # Ship must be placed in consecutive cells
    ALREADY_SET = 4   # Ship cannot be placed at same coordinate
    ALREADY_TRIED = 5 # Attack already made at coordinate
    OUT_OF_BOUNDS = 6 # Out of bounds of 10x10 grid

class Flag(Enum):
    """Enum that represents attack results

    Flag that indicates the result of an attack.
    """
    HIT = 0  # Attack was successful
    MISS = 1 # Attack was a miss
    SUNK = 2 # Ship has been sunk
