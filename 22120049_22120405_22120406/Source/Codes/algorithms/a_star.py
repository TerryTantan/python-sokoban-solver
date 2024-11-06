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
        stones = node.stones          # List of tuples (row, col, weight) for each stone
        switches = self.grid.switches # List of tuples (row, col) for each switch
        
        # Step 0: Initialize the cost matrix
        # For each stone-switch pair, calculate Manhattan distance * stone weight
        original_costs = []  # Keep original costs for final calculation
        cost_matrix = []     # Working matrix that will be modified
        for row_stone, col_stone, weight_stone in stones:
            row_costs = []
            original_row = []
            for row_switch, col_switch in switches:
                # Calculate Manhattan distance weighted by stone weight
                cost = (abs(row_switch - row_stone) + abs(col_switch - col_stone)) * weight_stone
                row_costs.append(cost)
                original_row.append(cost)  # Keep original cost for later
            cost_matrix.append(row_costs)
            original_costs.append(original_row)

        n = len(cost_matrix)  # Size of the matrix (number of stones/switches)
        
        # Arrays to keep track of covered rows and columns
        row_covered = [False] * n
        col_covered = [False] * n
        # Matrix to mark special zeros: 1=starred, 2=primed
        marked = [[0] * n for _ in range(n)]
        
        # Step 1: Row reduction
        # Subtract minimum value from each row to create zeros
        for i in range(n):
            row_min = min(cost_matrix[i])
            for j in range(n):
                cost_matrix[i][j] -= row_min

        # Step 2: Column reduction
        # Subtract minimum value from each column to create more zeros
        for j in range(n):
            col_min = min(cost_matrix[i][j] for i in range(n))
            for i in range(n):
                cost_matrix[i][j] -= col_min

        # Initial assignment: Star independent zeros
        self.cover_zeros(cost_matrix, row_covered, col_covered, marked, n)
        
        # Main loop of the Hungarian algorithm
        while self.covered_columns_count(col_covered) < n:
            # Try to find an uncovered zero
            row, col = self.find_uncovered_zero(cost_matrix, row_covered, col_covered, n)
            
            if row is None:
                # No uncovered zeros found
                # Find the smallest uncovered value to create new zeros
                min_uncovered = float('inf')
                for i in range(n):
                    for j in range(n):
                        if not row_covered[i] and not col_covered[j]:
                            min_uncovered = min(min_uncovered, cost_matrix[i][j])
                
                if min_uncovered == float('inf'):
                    break  # Safety check to prevent infinite loops
                    
                # Add min_uncovered to covered rows and subtract from uncovered columns
                # This creates new zeros while maintaining optimality
                for i in range(n):
                    for j in range(n):
                        if row_covered[i]:
                            cost_matrix[i][j] += min_uncovered
                        if not col_covered[j]:
                            cost_matrix[i][j] -= min_uncovered
            else:
                # Uncovered zero found - prime it
                marked[row][col] = 2
                # Look for a starred zero in the same row
                star_col = next((j for j in range(n) if marked[row][j] == 1), None)
                
                if star_col is None:
                    # No starred zero in this row
                    # Augment path starting from this primed zero
                    self.augment_path(marked, row, col, row_covered, col_covered, n)
                    # Reset all covers and remove prime markings
                    row_covered[:] = [False] * n
                    col_covered[:] = [False] * n
                    for i in range(n):
                        for j in range(n):
                            if marked[i][j] == 2:  # Remove primes
                                marked[i][j] = 0
                    # Cover columns containing starred zeros
                    for i in range(n):
                        for j in range(n):
                            if marked[i][j] == 1:
                                col_covered[j] = True
                else:
                    # Found starred zero in same row
                    # Cover this row and uncover the column with starred zero
                    row_covered[row] = True
                    col_covered[star_col] = False

        # Calculate total cost using original (unmodified) cost matrix
        total_cost = 0
        for i in range(n):
            for j in range(n):
                if marked[i][j] == 1:  # If this zero is starred (part of solution)
                    total_cost += original_costs[i][j]
        return total_cost

    def cover_zeros(self, cost_matrix, row_covered, col_covered, marked, n):
        """Find independent zeros and star them (mark with 1)"""
        for i in range(n):
            for j in range(n):
                if cost_matrix[i][j] == 0 and not row_covered[i] and not col_covered[j]:
                    marked[i][j] = 1  # Star this zero
                    row_covered[i] = True
                    col_covered[j] = True
        
        # Reset row covers as they're not needed for next phase
        row_covered[:] = [False] * n
        col_covered[:] = [False] * n
        
        # Cover columns containing starred zeros for next phase
        for j in range(n):
            for i in range(n):
                if marked[i][j] == 1:
                    col_covered[j] = True

    def covered_columns_count(self, col_covered):
        """Count how many columns are covered - used to check if we're done"""
        return sum(1 for col in col_covered if col)

    def find_uncovered_zero(self, cost_matrix, row_covered, col_covered, n):
        """Find a zero that is not covered by any line"""
        for i in range(n):
            for j in range(n):
                if cost_matrix[i][j] == 0 and not row_covered[i] and not col_covered[j]:
                    return i, j
        return None, None

    def augment_path(self, marked, start_row, start_col, row_covered, col_covered, n):
        """Find alternating path starting at a primed zero to augment the matching"""
        path = [(start_row, start_col)]
        
        while True:
            # Find a starred zero in the same column
            row = None
            for i in range(n):
                if marked[i][path[-1][1]] == 1:  # Starred zero found
                    row = i
                    break
                    
            if row is None:  # No starred zero found
                break
                
            path.append((row, path[-1][1]))
            
            # Find a primed zero in the same row
            col = None
            for j in range(n):
                if marked[row][j] == 2:  # Primed zero found
                    col = j
                    break
                    
            if col is None:  # No primed zero found
                break
                
            path.append((row, col))
        
        # Convert the path: unstar starred zeros and star unstarred zeros
        for row, col in path:
            if marked[row][col] == 1:
                marked[row][col] = 0  # Unstar
            else:
                marked[row][col] = 1  # Star