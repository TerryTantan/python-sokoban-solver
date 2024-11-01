from .base_search import BaseSearch
from ..data_structures.priority_queue import PriorityQueue
from ..core.grid import Grid
from ..core.node import Node
from scipy.optimize import linear_sum_assignment
import numpy as np


class AStar(BaseSearch):
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
        stones = node.stones
        switches = self.grid.switches
        heuristic = 0

        # Calculate the distance between each stone and the closest switch
        # Create cost matrix where rows represent stones and columns represent switches
        cost_matrix = np.zeros((len(stones), len(switches)))

        for i, (row_stone, col_stone, weight_stone) in enumerate(stones):
            for j, (row_switch, col_switch) in enumerate(switches):
                cost_matrix[i, j] = (
                    abs(row_switch - row_stone) + abs(col_switch - col_stone)
                ) * weight_stone

        # Use Hungarian algorithm to find the optimal assignment
        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        # Sum the minimum costs
        heuristic = cost_matrix[row_ind, col_ind].sum()

        return heuristic
