from algorithms.base_search import BaseSearch
from data_structures.priority_queue import PriorityQueue
from core.grid import Grid


class UCS(BaseSearch):
    def __init__(
        self, grid: Grid, next_node_data_structure: PriorityQueue = None
    ) -> None:
        if next_node_data_structure is None:
            next_node_data_structure = (
                PriorityQueue()
            )  # Create a new PriorityQueue if none is provided
        super().__init__(next_node_data_structure, grid)

    def calculate_g(self, node, push_cost) -> int:
        return node.parent.g_cost + push_cost

    def calculate_h(self, node) -> int:
        return 0
