from algorithms.base_search import BaseSearch
from data_structures.stack import Stack
from ..core.grid import Grid


class DFS(BaseSearch):
    def __init__(self, next_node_data_structure: Stack, grid: Grid) -> None:
        super().__init__(next_node_data_structure, grid)
