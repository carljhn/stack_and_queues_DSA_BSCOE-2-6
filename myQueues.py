# Now that you’ve chosen a suitable queue representation, you can fire up your favorite code editor, 
# such as Visual Studio Code or PyCharm, and create a new Python module for the different queue 
# implementations. You can call the file queues.py (plural form) to avoid a conflict with the similarly 
# named queue (singular form) module already available in Python’s standard library.

from collections import deque
from dataclasses import dataclass
from heapq import heapify, heappop, heappush
from itertools import count
from typing import Any

#Class IterableMixin
class IterableMixin:
    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        while len(self) > 0:
            yield self.dequeue()

#Class Queue
class Queue(IterableMixin):
    def __init__(self, *elements):
        self._elements = deque(elements)

    def enqueue(self, element):
        self._elements.append(element)
    
    def dequeue(self):
        return self._elements.popleft()