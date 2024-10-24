from algorithms.base_search import BaseSearch
from data_structures.priority_queue import PriorityQueue
from core.grid import Grid
from core.node import Node

class AStar(BaseSearch):
    def __init__(self, grid: Grid, next_node_data_structure: PriorityQueue = PriorityQueue()) -> None:
        super().__init__(next_node_data_structure, grid)

    def calculate_g(self, node, push_cost) -> int:
        return node.parent.g_cost + push_cost
    
    def calculate_h(self, node) -> int:
        stones = node.stones
        ares = node.position
        switches = self.grid.switches

        average_stone_weight = sum([stone[2] for stone in stones]) / len(stones)

        # Heuristic: sum of (the distances between each stone and the closest switch) * weight of the stone
        #          + sum of (the distances between the ares and the nearest stone that has not been on a switch yet)
        #          + punishment for not pushing the stone

        # Calculate the distance between the ares and the nearest stone that has not been on a switch yet
        heuristic = 0
        ares_heuristic_min = None
        for row_stone, col_stone, _ in stones:
            if (row_stone, col_stone) in switches:
                continue
            
            ares_heuristic = abs(row_stone - ares[0]) + abs(col_stone - ares[1])
            if ares_heuristic_min is None or ares_heuristic < ares_heuristic_min:
                ares_heuristic_min = ares_heuristic
        
        if ares_heuristic_min is not None:
            heuristic = ares_heuristic_min 

        heuristic *= average_stone_weight # Make the heuristic more accurate

        # Calculate the distance between each stone and the closest switch
        chosen_stones = [False] * len(stones)
        
        for row_switch, col_switch in switches:
            stone_heuristic_min = None

            for i, (row_stone, col_stone, weight_stone) in enumerate(stones):
                if chosen_stones[i]:
                    continue

                stone_heuristic = (abs(row_switch - row_stone) + abs(col_switch - col_stone)) * weight_stone
                if stone_heuristic_min is None or stone_heuristic < stone_heuristic_min:
                    stone_heuristic_min = stone_heuristic
                    chosen_stone_index = i

            chosen_stones[chosen_stone_index] = True

            if stone_heuristic_min is not None:
                heuristic += stone_heuristic_min
        return heuristic