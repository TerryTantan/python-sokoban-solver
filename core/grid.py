from copy import deepcopy
from ..configs.constants import MOVE_CHARS, MOVEMENTS, PUSH_CHARS, GridConstants


"""STATUS: Completed"""


class Grid:
    """
    The Grid class represents the game state of the Sokoban game. It includes methods to manage the positions
    of Ares (the player), stones, walls, and switches. The class also provides functionality for movement,
    checking valid moves, and determining if the game state is solved.

    Attributes:
        grid (list of list of str): The 2D grid representing the game board.
        ares_position (tuple): The (row, col) position of Ares.
        stones (list of tuple): List of positions of all stones in the grid.
        switches (list of tuple): List of positions of all switches in the grid.
        walls (list of tuple): List of positions of all walls in the grid.
    """

    def __init__(self, grid_data):
        """
        Initialize the grid for the Sokoban game.

        Args:
            grid_data (list of str): A list of strings where each string represents a row of the game grid.

        The characters in grid_data include:
            - '#' for walls
            - ' ' (whitespace) for free spaces
            - '$' for stones
            - '@' for Ares
            - '.' for switches
            - '*' for stones placed on switches
            - '+' for Ares on a switch
        """
        # Convert each row to a 2D list
        self.grid = [list(row) for row in grid_data]
        # Find the positions of Ares, stones, switches, and walls

        # Ares position is represented by '@' or '+'
        self.ares_position = self.find_position(
            GridConstants.ARES
        ) or self.find_position(GridConstants.ARES_ON_SWITCH)

        # Stones are represented by '$' or '*'
        self.stones = self.find_all_positions(
            GridConstants.STONE
        ) + self.find_all_positions(GridConstants.STONE_ON_SWITCH)

        # Switches are represented by '.' or '+' or '*'
        self.switches = (
            self.find_all_positions(GridConstants.SWITCH)
            + self.find_all_positions(GridConstants.ARES_ON_SWITCH)
            + self.find_all_positions(GridConstants.STONE_ON_SWITCH)
        )

        # Walls are represented by '#'
        self.walls = self.find_all_positions(GridConstants.WALL)

    def find_position(self, char):
        """
        Find the position of the first occurrence of a character in the grid.

        Args:
            char (str): The character to search for in the grid.

        Returns:
            tuple or None: The (row, col) position of the character if found, otherwise None.
        """
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell in enumerate(row):
                if cell == char:
                    return (row_idx, col_idx)
        return None

    def find_all_positions(self, char):
        """
        Find all positions of a character in the grid.

        Args:
            char (str): The character to search for in the grid.

        Returns:
            list of tuple: A list of (row, col) positions for each occurrence of the character.
        """
        positions = []
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell in enumerate(row):
                if cell == char:
                    positions.append((row_idx, col_idx))
        return positions

    def move_ares(self, direction):
        """
        Move Ares in a specified direction if the move is valid. If Ares encounters a stone, it will attempt
        to push it in the same direction.
        If the move is successful, the grid state is updated and the method returns True.
        If the move is invalid, the grid state remains unchanged and the method returns False.

        Args:
            direction (str): The direction to move Ares. Valid values are 'U' (up), 'D' (down), 'L' (left), 'R' (right).

        Returns:
            bool: True if the move is successful, False otherwise.
        """
        # Get the row and column deltas for the specified direction
        direction_delta = MOVEMENTS  # MOVEMENTS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}

        # Check if the direction is valid
        if direction not in direction_delta:
            return False

        delta_row, delta_col = direction_delta[direction]
        current_row, current_col = self.ares_position
        new_row, new_col = current_row + delta_row, current_col + delta_col

        # Check if the new position is valid
        if self.is_valid_position(new_row, new_col):
            # Move Ares to the new position
            if self.is_stone(new_row, new_col):
                # Try to push the stone
                if self.push_stone(new_row, new_col, delta_row, delta_col):
                    self.update_ares_position(new_row, new_col)
                    return True
                return False
            else:
                # Regular move
                self.update_ares_position(new_row, new_col)
                return True

        return False

    def is_stone(self, row, col):
        """
        Check if a position has a stone.

        :param row: Row index.
        :param col: Column index.
        :return: True if there is a stone, False otherwise.
        """
        return self.grid[row][col] in [
            GridConstants.STONE,
            GridConstants.STONE_ON_SWITCH,
        ]

    def is_valid_position(self, row, col):
        """
        Check if a specified position is valid for movement (i.e., it's not a wall).

        Args:
            row (int): The row index.
            col (int): The column index.

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        return (
            0 <= row < len(self.grid)
            and 0 <= col < len(self.grid[row])  # rows may have different number of cols
            and self.grid[row][col] != GridConstants.WALL
        )

    def push_stone(self, row, col, delta_row, delta_col):
        """
        Attempt to push a stone in the specified direction.

        :param row: Current row of the stone.
        :param col: Current column of the stone.
        :param delta_row: Row direction delta.
        :param delta_col: Column direction delta.
        :return: True if the stone was pushed successfully, False otherwise.
        """
        new_row, new_col = row + delta_row, col + delta_col

        # Check if the new stone position is valid
        # If the new position is not wall or stone then move the stone
        if self.is_valid_position(new_row, new_col) and not self.is_stone(
            new_row, new_col
        ):
            # Move the stone to the new position
            self.update_stone_position((row, col), (new_row, new_col))
            return True

        return False

    def update_ares_position(self, new_row, new_col):
        """
        Update Ares's position in the grid.

        :param new_row: New row index for Ares.
        :param new_col: New column index for Ares.
        """
        current_row, current_col = self.ares_position

        # Update the character on the old position of Ares
        if self.grid[current_row][current_col] == GridConstants.ARES_ON_SWITCH:
            self.grid[current_row][current_col] = GridConstants.SWITCH
        else:
            self.grid[current_row][current_col] = GridConstants.FREE_SPACE

        # Update the character on the new position of Ares
        if self.grid[new_row][new_col] == GridConstants.SWITCH:
            self.grid[new_row][new_col] = GridConstants.ARES_ON_SWITCH
        else:
            self.grid[new_row][new_col] = GridConstants.ARES

        self.ares_position = (new_row, new_col)

    def update_stone_position(self, old_pos, new_pos):
        """
        Update the position of a stone in the grid.

        :param old_pos: Tuple (row, col) of the current stone position.
        :param new_pos: Tuple (row, col) of the new stone position.
        """
        old_row, old_col = old_pos
        new_row, new_col = new_pos

        # Update the grid with the stone's new position

        # Update the character on the old position of the stone
        if self.grid[old_row][old_col] == GridConstants.STONE_ON_SWITCH:
            self.grid[old_row][old_col] = GridConstants.SWITCH
        else:
            self.grid[old_row][old_col] = GridConstants.FREE_SPACE

        # Update the character on the new position of the stone
        if self.grid[new_row][new_col] == GridConstants.SWITCH:
            self.grid[new_row][new_col] = GridConstants.STONE_ON_SWITCH
        else:
            self.grid[new_row][new_col] = GridConstants.STONE

    def is_goal(self):
        """
        Check if the current state is the goal state (all switches have stones).
        If all stones are placed on switches, the game is considered solved.
        Otherwise, the game is not yet solved.

        Returns:
            bool: True if the game is in a solved state, False otherwise.
        """
        for row, col in self.switches:
            if self.grid[row][col] not in [
                GridConstants.STONE_ON_SWITCH,
            ]:
                return False
        return True

    def copy(self):
        """
        Create a deep copy of the current grid state.
        Purpose: To create a copy of the grid state for simulation purposes.

        Returns:
            Grid: A new Grid object with the same state.
        """
        return Grid(deepcopy(self.grid))
