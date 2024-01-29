import random
from graph_interface import GraphComponentInterface


class Error(Exception):
    """
    Base class for exceptions in this module.
    """
    def __init__(self, message):
        """
        Constructor
        """
        self.message = message

    def to_dict(self):
        """
        Convert the error to a dictionary
        """
        return {"error": self.message}


class ClientGraph(GraphComponentInterface):
    """
    ClientGraph class
    """
    def __init__(self):
        self.cost_interval = {}
        self.graph_des = {}
        self.adj_list = {}
        self.adj_list_des = {}

    def graph(self, name, edges):
        """
        Graph method
        """
        # set a random cost interval for the graph
        self.cost_interval[name] = random.randint(10,30)

        class EdgeDescription:
            """
            EdgeDescription class
            """
            def __init__(self, from_node, to_node, cost=1):
                """
                Constructor
                """
                self.from_node = from_node
                self.to_node = to_node
                self.cost = cost

        edge_descriptions = []
        for edge in edges:
            from_node = edge.get("from_node")
            to_node = edge.get("to_node")
            cost = edge.get("cost", 1)

            if from_node is None:
                print(Error("from_node is missing").to_dict())
                continue
            if to_node is None:
                print(Error("to_node is missing").to_dict())
                continue
            if from_node == to_node:
                print(Error("from_node and to_node cannot be same").to_dict())
                continue

            # if graph name already exists
            if name in self.adj_list_des:
                self.adj_list = self.adj_list_des[name]
            if name in self.graph_des:
                edge_descriptions = self.graph_des[name]

            if self.add_edge_to_graph(name, from_node, to_node, cost):
                edge_description = EdgeDescription(from_node, to_node, cost)
                edge_descriptions.append(edge_description)

        self.graph_des[name] = edge_descriptions
        self.adj_list_des[name] = self.adj_list
        self.adj_list = {}  # reset the adj_list


    def join(self, graph_to_add, graph_to_join):
        """
        Join method
        """
        if graph_to_add in self.graph_des and graph_to_join in self.graph_des:
            if self.cost_interval[graph_to_join] >= self.cost_interval[graph_to_add]:
            # Get the nodes from both graphs
                nodes_graph_to_add = set()
                nodes_graph_to_join = set()
                for edge in self.graph_des[graph_to_add]:
                    nodes_graph_to_add.add(edge.from_node)
                    nodes_graph_to_add.add(edge.to_node)
                for edge in self.graph_des[graph_to_join]:
                    nodes_graph_to_join.add(edge.from_node)
                    nodes_graph_to_join.add(edge.to_node)

                # check disjoint
                if not nodes_graph_to_add.isdisjoint(nodes_graph_to_join):
                    # error
                    print(Error("The graphs are not disjoint").to_dict())
                    return
                else:
                    # extend the list
                    self.graph_des[graph_to_join].extend(self.graph_des[graph_to_add])
                    # update the edge in adj_list_des object
                    self.adj_list_des[graph_to_join].update(
                        self.adj_list_des[graph_to_add]
                    )

                    del self.cost_interval[graph_to_add]
                    # delete the graph_to_add from the graph_des object
                    del self.graph_des[graph_to_add]
                    # delete the graph_to_add from the adj_list_des object
                    del self.adj_list_des[graph_to_add]

            else:
                print(Error(f"Cost of {graph_to_add} does not lies with the range of {graph_to_join}").to_dict())
                return
        else:
            # error
            print(Error(f"{graph_to_add} or {graph_to_join} not found").to_dict())


    def add_edge_to_graph(self, name:str, source: str, target: str, cost: float) -> bool:
        """
        Method to add an edge to the graph
        """
        if cost <= 0.00:
            print(Error("Cost should be a positive real number").to_dict())
            return False
        if cost <= self.cost_interval[name]:
            if self.check_triangle_inequality(source, target, cost):
                if target not in self.adj_list:
                    self.adj_list[target] = {}
                if source in self.adj_list:
                    if target in self.adj_list[source]:
                        return False
                    else:
                        self.adj_list[source][target] = cost
                else:
                    self.adj_list[source] = {target: cost}
                return True
            else:
                print(Error(f"Triangle inequality does not hold true while adding {source} to {target}").to_dict())
                return False
        else:
            print(Error(f"Cost is greater than the cost interval for the edge {source} to {target}").to_dict())
            return False


    def get_neighbours(self, source: str):
        """
        Method to get the neighbours of a node
        """
        neighbours = []
        if source in self.adj_list:
            for vertex in self.adj_list[source]:
                neighbours.append(vertex)

        for vrt, edges in self.adj_list.items():
            if source in edges:
                neighbours.append(vrt)

        return neighbours


    def get_common_neighbours(self, source: str, target: str):
        """
        Method to get the common neighbours of two nodes
        """
        source_neighbours = self.get_neighbours(source)
        target_neighbours = self.get_neighbours(target)

        common_neighbours = set(source_neighbours).intersection(set(target_neighbours))

        return common_neighbours


    def check_triangle_inequality(self, source: str, target: str, cost: float):
        """
        Method to check if the triangle inequality is satisfied
        """
        common_neighbours = self.get_common_neighbours(source, target)
        for neighbour in common_neighbours:
            source_neighbour = self.get_traversal_cost(source, neighbour)
            if source_neighbour == float("inf"):
                source_neighbour = self.get_traversal_cost(neighbour, source)

            target_neighbour = self.get_traversal_cost(target, neighbour)
            if target_neighbour == float("inf"):
                target_neighbour = self.get_traversal_cost(neighbour, target)

            if (
                source_neighbour + target_neighbour < cost
                or source_neighbour + cost < target_neighbour
                or target_neighbour + cost < source_neighbour
            ):
                return False

        return True


    def get_traversal_cost(self, source: str, target: str) -> float:
        """
        Method to get the traversal cost from source to target
        """
        if source in self.adj_list:
            if target in self.adj_list[source]:
                return self.adj_list[source][target]

        return float("inf")


    def _is_node_present(self, node):
        """
        Check if the node is present in the graph_des object
        """
        for edges in self.graph_des.values():
            for edge in edges:
                if edge.from_node == node or edge.to_node == node:
                    return True
        return False


    def check_for_path(self, source, target):
        """
        Find all paths between two nodes
        """
        # if the source and target nodes are present in the graph
        if self._is_node_present(source) and self._is_node_present(target):
            paths = set()
            visited = set()
            self._find_all_paths(source, target, visited, [], paths)
            if paths:
                response = {"tag": "cost", "edges": []}
                for path in paths:
                    for i in range(len(path) - 1):
                        from_node = path[i]
                        to_node = path[i + 1]
                        for edge_list in self.graph_des.values():
                            for edge in edge_list:
                                if edge.from_node == from_node and edge.to_node == to_node:
                                    response["edges"].append(edge.__dict__)

                print(response)
            else:
                print("null")
        else:
            print(Error("Source or target node not found").to_dict())


    def _find_all_paths(self, current_node, target_node, visited, path, paths):
        """
        Helper method to find all paths between two nodes
        """
        visited.add(current_node)
        path.append(current_node)
        if current_node == target_node:
            paths.add(tuple(path))
        else:
            for edge_list in self.graph_des.values():
                for edge in edge_list:
                    if edge.from_node == current_node and edge.to_node not in visited:
                        self._find_all_paths(edge.to_node, target_node, visited, path, paths)
        path.pop()
        visited.remove(current_node)


if __name__ == "__main__":
    print("Running Client.py")
