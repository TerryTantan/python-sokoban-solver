from algorithms.base_search import BaseSearch
from data_structures.priority_queue import PriorityQueue
from core.grid import Grid


class UCS(BaseSearch):
    def __init__(self, grid: Grid, next_node_data_structure: PriorityQueue = PriorityQueue()) -> None:
        super().__init__(next_node_data_structure, grid)

    def calculate_g(self, node) -> int:
        return node.g_cost
    
    def calculate_h(self, node) -> int:
        return 0