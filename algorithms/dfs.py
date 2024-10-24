from algorithms.base_search import BaseSearch
from data_structures.stack import Stack
from core.grid import Grid


class DFS(BaseSearch):
    def __init__(self, grid: Grid, next_node_data_structure: Stack = Stack()) -> None:
        super().__init__(next_node_data_structure, grid)
