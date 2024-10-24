from copy import deepcopy


class Node:
    """
    A class to represent a node in the search algorithm.

    Attributes:
        position (tuple): A tuple representing the (row, column) position of Ares.
        stones (list): A list of tuples representing the positions of stones in the grid.
        parent (Node): The parent node from which this node was derived.
        action (str): The action taken to reach this node (e.g., 'u', 'd', 'l', 'r', 'U', 'D', 'L', 'R').
        g_cost (int): The cost to reach this node from the start node (for pathfinding algorithms).
        h_cost (int): The heuristic cost estimate to reach the goal from this node (for A* algorithm).
    """

    def __init__(
        self,
        position: tuple[int, int],
        stones: list[tuple[int, int, int]],
        parent=None,
        action: str = "",
        g_cost=0,
        h_cost=0,
        weight=0,
    ):
        """
        Initializes a Node with the given parameters.

        Args:
            position (tuple): The (row, column) position of Ares.
            stones (list of tuple(row, col, weight)): The current positions of stones on the grid.
            parent (Node, optional): The parent node. Defaults to None.
            action (str, optional): The action taken to reach this node. Defaults to None.
            g_cost (int, optional): The cost to reach this node. Defaults to 0.
            h_cost (int, optional): The heuristic cost to reach the goal. Defaults to 0.
        """
        self.position = deepcopy(position)
        self.stones = deepcopy(stones)
        self.parent = parent
        self.action = deepcopy(action)
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.weight = weight

    def __eq__(self, other):
        """Check if two nodes are equal based on their position and stones."""
        return (self.position == other.position) and (self.stones == other.stones)

    def __hash__(self):
        """Generate a hash for the node based on its position and stones."""
        return hash((self.position, tuple(self.stones)))

    def total_cost(self) -> int:
        """Calculate the total cost of the node (g_cost + h_cost)."""
        return self.g_cost + self.h_cost

    def get_path(self):
        """Retrieve the path of actions taken to reach this node from the start node."""
        path = []
        current_node = self
        while current_node:
            if current_node.action:
                path.append(current_node.action)
            current_node = current_node.parent
        return path[::-1]  # Reverse the path to get the correct order

    def __str__(self) -> str:
        return f"Node: {self.position}, Stones: {self.stones}, Cost: {self.total_cost()}, Action: {self.action}"
    
    def __lt__(self, other):
        """Return True if the data structure is less than the other data structure."""
        return True
