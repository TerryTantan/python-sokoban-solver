# constants.py

# Movement directions with their corresponding row and column deltas
MOVEMENTS = {
    "U": (-1, 0),  # Up
    "D": (1, 0),  # Down
    "L": (0, -1),  # Left
    "R": (0, 1),  # Right
}

# Movement characters for actions
MOVE_CHARS = {"UP": "u", "DOWN": "d", "LEFT": "l", "RIGHT": "r"}

# Push actions for stones
PUSH_CHARS = {"UP": "U", "DOWN": "D", "LEFT": "L", "RIGHT": "R"}


class GridConstants:
    """
    A class to hold constant values representing different states in the grid.
    Each constant corresponds to a specific character used in the grid.
    The characters in grid_data include:
    - '#' for walls
    - ' ' (whitespace) for free spaces
    - '$' for stones
    - '@' for Ares
    - '.' for switches
    - '*' for stones placed on switches
    - '+' for Ares on a switch
    """

    WALL = "#"
    FREE_SPACE = " "  # Whitespace for free spaces
    STONE = "$"
    ARES = "@"
    SWITCH = "."
    STONE_ON_SWITCH = "*"
    ARES_ON_SWITCH = "+"
