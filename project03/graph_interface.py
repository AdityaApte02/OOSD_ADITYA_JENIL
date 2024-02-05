from abc import ABC, abstractmethod

class GraphComponentInterface(ABC):
    @abstractmethod
    def add_edge_to_graph(self, name:str, source:str, target:str, cost:float) -> tuple:
        # Checks for traingular inequality, and checks if the cost is not exceeding cost interval.
        # If both are satisified, adds an edge from source to target with the given cost and returns True
        # If any one is not satisfied, returns False
        # source: Source node
        # target: Target node
        # cost: cost of the edge from Source to Target
        pass

    @abstractmethod
    def join(self, graph_to_add: 'GraphComponentInterface', graph_to_join: 'GraphComponentInterface') -> None:
        # Checks if the graph_to_add and graph_to_join have same disjoint set of Nodes and operate on the same cost interval.
        # If both are satisfied, joins graph_to_add and graph_to_join
        # graph_to_add: Graph that needs to be joined.
        # graph_to_join: Graph that needs to be joined.
        pass

    @abstractmethod
    def get_traversal_cost(self, source:str, target:str) -> float:
        # Checks if there is a path from source to target. If there is a path, returns the cost of the path.
        # Else, returns -infinity
        # source: source Node
        # target: target Node
        pass

    @abstractmethod
    def check_for_path(self, source:str, target:str) -> bool:
        # Checks if there is a path from source to target. If there is a path, returns True.
        # Else, returns False.
        # source: source Node
        # target: target Node
        pass