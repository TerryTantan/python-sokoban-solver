from abc import ABC, abstractmethod
from ..core.node import Node
from collections import deque


class BaseDataStructure(ABC):
    def __init__(self, container: list | deque):
        self.container = container

    @abstractmethod
    def add(self, item: Node):
        """Add an item to the data structure."""
        pass

    @abstractmethod
    def pop(self) -> Node:
        """Remove and return an item from the data structure."""
        pass

    def is_empty(self) -> bool:
        """Check if the data structure is empty."""
        return len(self.container) == 0

    def __contains__(self, item: Node) -> bool:
        """Check if the data structure contains the given item."""
        return item in self.container

    def __len__(self):
        """Return the number of items in the data structure."""
        return len(self.container)

