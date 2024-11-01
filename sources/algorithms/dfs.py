from .base_search import BaseSearch
from ..data_structures.stack import Stack
from ..core.grid import Grid


class DFS(BaseSearch):
    def __init__(self, grid: Grid, next_node_data_structure: Stack = None) -> None:
        if next_node_data_structure is None:
            next_node_data_structure = Stack()  # Create a new Stack if none is provided
        super().__init__(next_node_data_structure, grid)

    def calculate_g(self, node, push_cost) -> int:
        return 0

    def calculate_h(self, node) -> int:
        return 0
