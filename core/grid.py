from copy import deepcopy
from configs.constants import MOVE_CHARS, MOVEMENTS, PUSH_CHARS, GridConstants


"""STATUS: Completed"""


class Grid:
    """
    The Grid class represents the game state of the Sokoban game. It includes methods to manage the positions
    of Ares (the player), stones, walls, and switches. The class also provides functionality for movement,
    checking valid moves, and determining if the game state is solved.

    Parameters:
        weight_data (str): The weights of each stone in the grid from top left to bottom right.
        grid_data (list of str): A list of strings where each string represents a row of the game grid

    Attributes:
        weights (list of int): The weights of each stone in the grid from top left to bottom right.
        grid (list of list of str): The 2D grid representing the game board.
        ares_position (tuple): The (row, col) position of Ares.
        stones (list of tuple): List of positions of all stones in the grid. Each stone is represented by a tuple (row, col, weight).
        switches (list of tuple): List of positions of all switches in the grid.
        walls (list of tuple): List of positions of all walls in the grid.
    """

    def __init__(self, weight_data: str, grid_data: list):
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
        # Convert the weight data to a list of integers
        self.weights = list(map(int, weight_data.split()))

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

        # Sort the stones row increasing and then column increasing
        self.stones = sorted(self.stones, key=lambda x: (x[0], x[1]))

        # Combine the stones with their weights
        self.stones = {
            (row, col): weight for (row, col), weight in zip(self.stones, self.weights)
        }

        self.current_stones = deepcopy(self.stones)

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

    def move_ares(
        self,
        direction: str,
        # update: bool = True,
        weight: list[int] = [0],
    ) -> str | None:
        """
        Move Ares in a specified direction if the move is valid. If Ares encounters a stone, it will attempt
        to push it in the same direction.
        If the move is successful, the grid state is updated and the method returns True.
        If the move is invalid, the grid state remains unchanged and the method returns False.

        Args:
            direction (str): The direction to move Ares. Valid values are 'U' (up), 'D' (down), 'L' (left), 'R' (right).

        Returns:
            str or None: The direction moved in lowercase if successful, otherwise
            int: The weight of the stone that was pushed.
        """
        # Get the row and column deltas for the specified direction
        direction_delta = MOVEMENTS  # MOVEMENTS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}

        # Check if the direction is valid
        if direction not in direction_delta:
            return None, None

        delta_row, delta_col = direction_delta[direction]
        current_row, current_col = self.ares_position
        new_row, new_col = current_row + delta_row, current_col + delta_col

        # Check if the new position is valid
        if self.is_valid_position(new_row, new_col):
            # Move Ares to the new position
            if self.is_stone(new_row, new_col):
                # Try to push the stone
                if self.push_stone(new_row, new_col, delta_row, delta_col, weight):
                    pushCost = self.get_stone_weight(
                        new_row + delta_row, new_col + delta_col
                    )
                    self.update_ares_position(new_row, new_col)
                    return direction, pushCost
                return None, 0
            else:
                # Regular move
                self.update_ares_position(new_row, new_col)
                return direction.lower(), 0

        return None, None

    def get_stone_weight(self, row, col):
        """Get the weight of a stone at the specified (row, col) position."""
        return self.current_stones.get(
            (row, col), 0
        )  # Returns 0 if (row, col) is not found

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

    def push_stone(
        self,
        row,
        col,
        delta_row,
        delta_col,
        # update: bool = True,
        weight: list[int] = [0],
    ):
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
        # If the new position is not wall or stone and not a deadlock then move the stone
        if (
            self.is_valid_position(new_row, new_col)
            and not self.is_stone(new_row, new_col)
            and not self.is_deadlock(new_row, new_col)
        ):
            # Move the stone to the new position
            # if update:
            weight[0] += self.update_stone_position((row, col), (new_row, new_col))
            return True

        return False

    def is_deadlock(self, row, col):
        """
        Check if a stone is in a deadlock position.

        :param row: Row index of the stone.
        :param col: Column index of the stone.
        """
        # The stone is in a deadlock position if
        # - It is surrounded by walls on three sides and not on a switch
        # - It is surrounded by walls on two consecutive sides and not on a switch
        if self.grid[row][col] == GridConstants.SWITCH:
            return False

        # Calculate the directions in which the stone is surrounded by walls
        directions_surrounded_by_walls = []
        for delta_row, delta_col in MOVEMENTS.values():
            new_row, new_col = row + delta_row, col + delta_col
            if self.grid[new_row][new_col] == GridConstants.WALL:
                directions_surrounded_by_walls.append((delta_row, delta_col))

        if len(directions_surrounded_by_walls) >= 3:
            return True

        if len(directions_surrounded_by_walls) < 2:
            return False

        # Check if the stone is surrounded by walls on two consecutive sides
        if (
            directions_surrounded_by_walls[0][0] + directions_surrounded_by_walls[1][0]
            == 0
        ) and (
            directions_surrounded_by_walls[0][1] + directions_surrounded_by_walls[1][1]
            == 0
        ):
            return False
        return True

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

    def update_stone_position(self, old_pos, new_pos) -> int:
        """
        Update the position of a stone in the grid.

        :param old_pos: Tuple (row, col) of the current stone position.
        :param new_pos: Tuple (row, col) of the new stone position.
        :return: The weight of the moved stone.
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

        # Retrieve and update the stone's weight in the dictionary
        weight = self.current_stones.pop(old_pos, 0)  # Remove the old position
        self.current_stones[new_pos] = weight  # Add the new position

        return weight

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

    def reset_grid(
        self,
        new_ares_position: tuple[int, int],
        new_stones_positions: list[tuple[int, int, int]],
    ):
        """
        Reset the grid to the initial state with the specified Ares position and stone positions.

        Args:
            new_ares_position (row, col): The new position of Ares.
            new_stones_positions (list of tuple(row, col, weight)): The new positions of the stones.
        """
        # Reset all position to free space, except walls and switches
        # for row_idx, row in enumerate(self.grid):
        #     for col_idx, cell in enumerate(row):
        #         if cell not in [GridConstants.WALL]:
        #             self.grid[row_idx][col_idx] = GridConstants.FREE_SPACE

        # # Set all switch positions to normal switch
        # for row, col in self.switches:
        #     self.grid[row][col] = GridConstants.SWITCH

        # 1. Reset previous Ares position
        if self.ares_position:
            row, col = self.ares_position
            self.grid[row][col] = (
                GridConstants.SWITCH
                if (row, col) in self.switches
                else GridConstants.FREE_SPACE
            )

        # 2. Reset previous stones positions
        if self.current_stones:
            for (row, col), weight in self.current_stones.items():
                self.grid[row][col] = (
                    GridConstants.SWITCH
                    if (row, col) in self.switches
                    else GridConstants.FREE_SPACE
                )

        # Update the new Ares position
        # If Ares is on a switch, update the switch character
        if (
            self.grid[new_ares_position[0]][new_ares_position[1]]
            == GridConstants.SWITCH
        ):
            self.grid[new_ares_position[0]][new_ares_position[1]] = (
                GridConstants.ARES_ON_SWITCH
            )
        else:
            self.grid[new_ares_position[0]][new_ares_position[1]] = GridConstants.ARES

        # Update the new stone positions
        # If a stone is on a switch, update the switch character
        for new_row, new_col, weight in new_stones_positions:
            if self.grid[new_row][new_col] == GridConstants.SWITCH:
                self.grid[new_row][new_col] = GridConstants.STONE_ON_SWITCH
            else:
                self.grid[new_row][new_col] = GridConstants.STONE

        # self.current_stones = deepcopy(new_stones_positions)
        self.current_stones = {
            (row, col): weight for row, col, weight in new_stones_positions
        }
        self.ares_position = deepcopy(new_ares_position)

    def copy(self):
        """
        Create a deep copy of the current grid state.
        Purpose: To create a copy of the grid state for simulation purposes.

        Returns:
            Grid: A new Grid object with the same state.
        """
        return Grid(deepcopy(self.grid))

    def __str__(self):
        """
        Return a string representation of the grid.

        Returns:
            str: A string representation of the grid.
        """
        return "\n".join("".join(row) for row in self.grid)
