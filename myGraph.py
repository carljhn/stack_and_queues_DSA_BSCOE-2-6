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

#Class City
class City(NamedTuple):
    name: str
    country: str
    year: int | None
    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, attrs):
        return cls (
            name = attrs["xlabels"],
            country = attrs["country"],
            year = int(attrs["year"]) or None, 
            latitude = float(attrs["latitude"]),
            longtitude = float(attrs["longitude"]),
        )

#Function load_graph
def load_graph(filename, node_factory):
    graph = nx.nx_agraph.read_dot(filename)
    nodes = {
        name: node_factory(attributes)
        for name, attributes in graph.nodes(data = True)
    }
    return nodes, nx.Graph(
        (nodes[name1], nodes[name2], weights)
        for name1, name2, weights in graph.edges(data = True)
    )

#Function breadth_first_traverse
def breadth_first_traverse(graph, source, order_by = None):
    queue = Queue(source)
    visited = {source}
    while queue:
        yield (node := queue.dequeue())
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key = order_by)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)

#function breadth_first_search
def breadth_first_search(graph, source, predicate, order_by = None):
    return search(breadth_first_traverse, graph, source, predicate, order_by)

#Function shortest_path
def shortest_past(graph, source, destination, order_by = None):
    queue = Queue(source)
    visited = {source}
    previous = {}
    while queue:
        node = queue.dequeue()
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key = order_by)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)
                previous[neighbor] = node
                if neighbor == destination:
                    return retrace(previous, source, destination)

#Function retrace
def ratrace(previous, source, destination):
    path = deque()
    current = destination
    while current != source:
        path.appendleft(current)
        current = previous.get(current)
        if current is None:
            return None
    
    path.appendleft(source)
    return list(path)

#Function connected
def connected(graph, source, destination):
    return shortest_past(graph, source, destination) is not None

#Function depth_first_traverse
def depth_first_traverse(graph, source, order_by = None):
    stack = Stack(source)
    visited = set()
    while stack:
        if (node := stack.dequeue()) not in visited:
            yield node
            visited.add(node)
            neighbors = list(graph.neighbors(node))
            if order_by:
                neighbors.sort(key = order_by)
            for neighbor in reversed(neighbors):
                stack.enqueue(neighbor)

#Function recursive_depth_first_traverse
def recursive_depth_first_traverse(graph, source, order_by = None):
    visited = set()
    def visit(node):
        yield node
        visited.add(node)
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key = order_by)
        for neighbor in neighbors:
            if neighbor not in visited:
                yield from visit(neighbor)

    return visit(source)