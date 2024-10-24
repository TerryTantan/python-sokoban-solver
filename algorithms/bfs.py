from algorithms.base_search import BaseSearch
from data_structures.queue import Queue
from core.grid import Grid


class BFS(BaseSearch):
    def __init__(self, grid: Grid, next_node_data_structure: Queue = Queue()) -> None:
        super().__init__(next_node_data_structure, grid)
