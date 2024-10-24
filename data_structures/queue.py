from data_structures.base_data_structure import BaseDataStructure
from core.node import Node
from collections import deque


class Queue(BaseDataStructure):
    def __init__(self):
        super().__init__(container=deque[Node]())

    def add(self, item: Node):
        """Enqueue an item into the queue."""
        self.container.append(item)

    def pop(self) -> Node:
        """Dequeue an item from the queue."""
        if self.is_empty():
            raise IndexError("Pop from empty queue")
        return self.container.popleft()  # FIFO behavior
