# In this section, you’re going to use the queues that you just built to implement 
# classic graph traversal algorithms. There are numerous ways to represent graphs 
# in code and an equal number of Python libraries that already do that well. 
# For the sake of simplicity, you’ll take advantage of the networkx and pygraphviz 
# libraries, as well as the widely used DOT graph description language.

from collections import deque
from math import inf as infinity
from typing import NamedTuple

import networkx as nx
from queues import MutableMinHeap, Queue, Stack