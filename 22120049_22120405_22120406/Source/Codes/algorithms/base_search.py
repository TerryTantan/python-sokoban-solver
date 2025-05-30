from ..data_structures.base_data_structure import BaseDataStructure
from ..core.grid import Grid
from ..core.node import Node
from ..configs.constants import MOVEMENTS
import time
import tracemalloc
from abc import ABC, abstractmethod
from time import sleep


class Solution:
    """
    Represents the result of a search algorithm in terms of steps, weight,
    node count, execution time, memory usage, and the path to the goal.

    Attributes:
        steps (int): The number of steps taken to reach the goal.
        weight (int): The total weight or cost of the path to the goal.
        node_count (int): The total number of nodes visited during the search.
        time (float): The execution time of the search algorithm in milliseconds.
        memory (float): The peak memory usage of the search algorithm in MB.
        path (str): The sequence of actions or moves taken to reach the goal state.

    Methods:
        __str__(): Returns a formatted string representation of the solution,
                   including the steps, weight, node count, execution time,
                   memory usage, and path.
    """

    def __init__(
        self, steps: int, weight: int, node_count: int, time, memory: float, path: str
    ) -> None:
        self.steps = steps
        self.weight = weight
        self.node_count = node_count
        self.time = time
        self.memory = memory
        self.path = path

    def __str__(self) -> str:
        return (
            f"Steps: {self.steps}, Weight: {self.weight}, Node: {self.node_count}, "
            f"Time (ms): {self.time:.2f}, Memory (MB): {self.memory:.2f}\n{self.path}"
        )


class BaseSearch(ABC):
    def __init__(self, next_node_data_structure: BaseDataStructure, grid: Grid) -> None:
        self.next_node_data_structure = next_node_data_structure
        self.grid = grid
        self.visited = set[Node]()  # Set of visited nodes
        self.node_count = 0  # Number of nodes visited
        self.weight = [0]
        self.path = ""  # Path to the goal state
        self.execution_time = 0.0  # To store execution time in milliseconds
        self.memory_used = 0.0  # To store peak memory usage in MB
        # Start memory tracking
        tracemalloc.start()

        self.start_time = time.perf_counter()

    def search(self) -> bool:
        # print("Len before search: " + str(len(self.next_node_data_structure)))
        init_node = Node(
            position=self.grid.ares_position,
            stones=sorted(
                [(row, col, weight) for (row, col), weight in self.grid.stones.items()],
                key=lambda x: (x[0], x[1]),  # Sort by row, then by column
            ),
        )
        self.next_node_data_structure.add(init_node)

        flag = False

        while not self.next_node_data_structure.is_empty():
            node = self.next_node_data_structure.pop()
            self.node_count += 1

            self.visited.add(node)

            if self.is_goal_state(node):
                self.path = "".join(node.get_path())
                self.result_weight = node.weight
                flag = True
                break

            for direction in MOVEMENTS:
                self.grid.reset_grid(node.position, node.stones)
                child_node = self.perform_move(node, direction)

                if child_node is not None and child_node not in self.visited:
                    self.next_node_data_structure.add(child_node)

        # Stop the timer
        self.end_time = time.perf_counter()

        # Stop memory tracking and get peak memory
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Calculate time and memory usage
        self.execution_time = (
            self.end_time - self.start_time
        ) * 1000  # Convert to milliseconds
        self.memory_used = peak_memory / (1024 * 1024)  # Convert to MB

        self.solution = Solution(
            len(self.path),
            self.result_weight,
            self.node_count,
            self.execution_time,
            self.memory_used,
            self.path,
        )

        return flag

    def perform_move(self, node: Node, direction: str) -> Node | None:
        """
        Perform an action on the current node.

        Args:
            node (Node): The current node.
            direction (str): The action to be performed.

        Returns:
            Node: The resulting node after performing the action.
        """
        prev_weight = self.weight[0]
        action, push_cost = self.grid.move_ares(direction, weight=self.weight)

        if not action:
            return None

        # Create new node
        new_node = Node(
            position=self.grid.ares_position,
            stones=sorted(
                [
                    (row, col, weight)
                    for (row, col), weight in self.grid.current_stones.items()
                ],
                key=lambda x: (x[0], x[1]),  # Sort by row, then by column
            ),
            parent=node,
            action=action,
            weight=node.weight + self.weight[0] - prev_weight,
        )

        new_node.g_cost = self.calculate_g(new_node, push_cost)
        new_node.h_cost = self.calculate_h(new_node)

        return new_node

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

    def get_solution(self) -> Solution:
        return self.solution

    def get_path(self) -> str:
        return self.path

    @abstractmethod
    def calculate_g(self, node: Node, push_cost: int) -> int:
        """Calculate the cost from the start node to the current node."""
        pass

    @abstractmethod
    def calculate_h(self, node: Node) -> int:
        """Calculate the heuristic cost from the current node to the goal node."""
        pass
