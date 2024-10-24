from data_structures.base_data_structure import BaseDataStructure
from core.grid import Grid
from core.node import Node
from configs.constants import MOVEMENTS
import time
import tracemalloc


class Solution:
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


class BaseSearch:
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
        init_node = Node(self.grid.ares_position, self.grid.stones)
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
        action = self.grid.move_ares(direction, weight=self.weight)
        # print(action)
        # print(self.grid.ares_position)

        if not action:
            return None

        return Node(
            self.grid.ares_position,
            self.grid.current_stones,
            node,
            action,
            self.calculate_g(node),
            self.calculate_h(node),
            node.weight + self.weight[0] - prev_weight,
        )

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

    def calculate_g(self, node: Node) -> int:
        return 0

    def calculate_h(self, node: Node) -> int:
        return 0
