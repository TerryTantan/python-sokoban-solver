from algorithms.base_search import BaseSearch
from data_structures.queue import Queue
from ..core.grid import Grid


class BFS(BaseSearch):
    def __init__(self, next_node_data_structure: Queue, grid: Grid) -> None:
        super().__init__(next_node_data_structure, grid)
