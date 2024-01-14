```python
from abc import ABC, abstractmethod

class Node:

    def __init__(self, label) -> None:
        self.label = label
        self.adjacencyList = {}

class GraphComponentInterface(ABC):

    @abstractmethod
    def __init__(self, cost_interval) -> None:
        self.cost_interval = cost_interval

    @abstractmethod
    def addEdgeToGraph(self, source:Node, target:Node, cost:float) -> bool:

        # Checks for traingular inequality, and checks if the cost is not exceeding cost interval.
        # If both are satisified, adds an edge from source to target with the given cost and returns True
        # If any one is not satisfied, returns False
        # source: Source node
        # target: Target node
        # cost: cost of the edge from Source to Target

        pass

    @abstractmethod
    def joinTwoGraphs(self, graph1: 'GraphComponentInterface', graph2: 'GraphComponentInterface') -> None:

        # Checks if the graph1 and graph2 have same disjoint set of Nodes and operate on the same cost interval.
        # If both are satisfied, joins graph1 and graph2
        # graph1: Graph1 that needs to be joined.
        # graph2: Graph2 that needs to be joined.

        pass

    @abstractmethod
    def getTraversalCost(self, source:Node, target:Node) -> float:

        # Checks if there is a path from source to target. If there is a path, returns the cost of the path.
        # Else, returns -infinity
        # source: source Node
        # target: target Node

        pass

    @abstractmethod
    def checkForPath(self, source:Node, target:Node) -> bool:

        # Checks if there is a path from source to target. If there is a path, returns True.
        # Else, returns False.
        # source: source Node
        # target: target Node

        pass
```
