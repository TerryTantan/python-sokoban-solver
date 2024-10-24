from algorithms.base_search import BaseSearch
from core.node import Node
from data_structures.queue import Queue
from core.grid import Grid


class BFS(BaseSearch):
    def __init__(self, grid: Grid, next_node_data_structure: Queue = Queue()) -> None:
        super().__init__(next_node_data_structure, grid)

    def calculate_g(self, node, push_cost) -> int:
        return 0
    
    def calculate_h(self, node) -> int:
        return 0
