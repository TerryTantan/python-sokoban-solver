from .base_data_structure import BaseDataStructure
from ..core.node import Node
import heapq


class PriorityQueue(BaseDataStructure):
    def __init__(self):
        super().__init__(container=[])

    def add(self, item: Node):
        """Add an item to the priority queue."""
        heapq.heappush(self.container, (item.total_cost(), item))

    def pop(self) -> Node:
        """Remove and return the item with the lowest cost from the priority queue."""
        if self.is_empty():
            raise IndexError("Pop from empty priority queue")
        return heapq.heappop(self.container)[1]