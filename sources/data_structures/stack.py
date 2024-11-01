from .base_data_structure import BaseDataStructure
from ..core.node import Node
from collections import deque


class Stack(BaseDataStructure):
    def __init__(self):
        super().__init__(container=deque[Node]())

    def add(self, item: Node):
        """Push an item onto the stack."""
        self.container.append(item)

    def pop(self) -> Node:
        """Pop an item from the stack."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self.container.pop()  # LIFO behavior
