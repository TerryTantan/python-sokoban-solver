from ..data_structures.base_data_structure import BaseDataStructure
from ..core.grid import Grid
from ..core.node import Node
from ..configs.constants import MOVEMENTS


class BaseSearch:
    def __init__(self, next_node_data_structure: BaseDataStructure, grid: Grid) -> None:
        self.next_node_data_structure = next_node_data_structure
        self.grid = grid
        self.visited = set[Node]()  # Set of visited nodes
        self.solution = list[str]()  # List of actions leading to the solution
        self.node_count = 0  # Number of nodes visited

    def search(self) -> bool:
        init_node = Node(self.grid.ares, self.grid.stones)
        self.next_node_data_structure.add(init_node)

        while not self.next_node_data_structure.is_empty():
            node = self.next_node_data_structure.pop()
            self.node_count += 1

            self.grid.reset_grid(node.position, node.stones)

            if self.is_goal_state(node):
                self.solution = node.get_path()
                self.steps = len(self.solution)
                return True

            self.visited.add(node)

            for direction in MOVEMENTS:
                child_node = self.perform_move(node, direction)

                if child_node is not None and child_node not in self.visited:
                    self.next_node_data_structure.add(child_node)

        return False

    def perform_move(self, node: Node, direction: str) -> Node | None:
        """
        Perform an action on the current node.

        Args:
            node (Node): The current node.
            direction (str): The action to be performed.

        Returns:
            Node: The resulting node after performing the action.
        """

        action = self.grid.move_ares(direction, update=False)

        if action is None:
            return None

        return Node(self.grid.ares_position, self.grid.stones, node, action, 0, 0)

    def is_goal_state(self, node: Node) -> bool:
        """
        Checks if the current node is the goal state.

        Args:
            node (Node): The current node.

        Returns:
            bool: True if the goal state is reached, False otherwise.
        """
        # Implement the logic to check if all stones are on switches
        # For example:
        count = 0
        for [rol, col, weight] in node.stones:
            if (rol, col) in self.grid.switches:
                count += 1

        return count == len(self.grid.switches)
