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

    def is_real_number(self, num):
        """
        Check if the number is a real number
        """
        try:
            float(num)
            return True
        except ValueError:
            return False
    
    def add_graph(self, low, high, name):
        """
        AddGraph method
        """
        if name is None or name == "":
            return (Error("name is missing"))
        if name in self.cost_interval:
            return (Error(f"Graph {name} already exists"))
        if self.is_real_number(str(low)):
            low = float(low)
        else:
            return (Error("Low should be a positive real number"))
        if self.is_real_number(str(high)):
            high = float(high)
        else:
            return (Error("High should be a positive real number"))
        if low < 0 or high < 0:
            return (Error("Cost interval should be a positive real number"))
        if low >= high:
            return (Error("Low should be less than high"))
        self.cost_interval[name] = (low, high)
        self.graph_des[name] = []
        self.adj_list_des[name] = {}
        print("cost interval",self.cost_interval)

    def graph(self, name, from_node, to_node, cost):
        """
        Graph method
        """
        # Check if the graph name already exists
        # if name in self.graph_des:
        #     print(Error(f"{name} already exists").to_dict())
        #     return

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
        if name is None or name == "":
            return (Error("Graph name is missing"))
        if name not in self.adj_list_des:
            return (Error(f"{name} graph is not created yet"))
        if from_node is None or from_node == "":
            return (Error("from_node is missing"))
        if to_node is None or to_node == "":
            return (Error("to_node is missing"))
        if from_node == to_node:
            return (Error("from_node and to_node cannot be same"))
        if self.is_real_number(str(cost)) and float(cost) > 0.00:
            cost = float(cost)
        else:
            return (Error("Cost should be a positive real number"))

        # if graph name already exists
        if name in self.adj_list_des:
            self.adj_list = self.adj_list_des[name]
        if name in self.graph_des:
            edge_descriptions = self.graph_des[name]
        
        res = self.add_edge_to_graph(name, from_node, to_node, cost)
        if res[0]:
            edge_description = EdgeDescription(from_node, to_node, cost)
            edge_descriptions.append(edge_description)

            self.graph_des[name] = edge_descriptions
            self.adj_list_des[name] = self.adj_list
            self.adj_list = {}  # reset the adj_list

        else:
            return res[1]

        # debug start
        print()
        print("adj_list_des:")
        print(self.adj_list_des)
        print("Cost Interval:")
        print(self.cost_interval)
        print("Graph Description:")
        print(self.graph_des)
        print()
        # debug end

    def join(self, graph_to_add, graph_to_join):
        """
        Join method
        """
       
        if graph_to_add in self.graph_des and graph_to_join in self.graph_des:
            if self.cost_interval[graph_to_join][0] <= self.cost_interval[graph_to_add][0] and self.cost_interval[graph_to_join][1] >= self.cost_interval[graph_to_add][1]:
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
                    return (Error("The graphs are not disjoint"))
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

                    # debug start
                    print()
                    print("join complete")
                    print("adj_list_des:")
                    print(self.adj_list_des)
                    print()

            else:
                print('Interval not compatible')
                return (Error(f"Cost of {graph_to_add} does not lies with the range of {graph_to_join}"))
        else:
            # error
            return (Error(f"{graph_to_add} or {graph_to_join} not found"))


    def add_edge_to_graph(self, name:str, source: str, target: str, cost: float) -> bool:
        """
        Method to add an edge to the graph
        """
        if cost <= self.cost_interval[name][1] and cost >= self.cost_interval[name][0]:
            if self.check_triangle_inequality(source, target, cost):
                if target not in self.adj_list:
                    self.adj_list[target] = {}
                if source in self.adj_list:
                    if target in self.adj_list[source]:
                        return (False, Error(f"The edge {source} to {target} already exists"))
                    else:
                        self.adj_list[source][target] = cost
                else:
                    self.adj_list[source] = {target: cost}
                return (True, None)
            else:
                return (False, Error(f"Triangle inequality does not hold true while adding {source} to {target}"))
        else:
            return (False, Error(f"Cost is not in the cost interval range while adding the edge {source} to {target}"))
        

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

    def check_for_path(self, graph_name, source, target):
        """
        Find all paths between two nodes
        """
        if graph_name in self.graph_des:
            if self._is_node_present(source) and self._is_node_present(target):
                visited = set()
                path = []
                paths = set()
                self._find_all_paths(graph_name, source, target, visited, path, paths)
                if paths:
                    response = {"cost": float('inf'), "edges": []}
                    for path in paths:
                        total_cost = 0
                        for i in range(len(path) - 1):
                            from_node = path[i]
                            to_node = path[i + 1]
                            for edge in self.graph_des[graph_name]:
                                if edge.from_node == from_node and edge.to_node == to_node:
                                    total_cost += edge.cost
                                    response["edges"].append(edge)
                        if total_cost < response["cost"]:
                            response["cost"] = total_cost

                    return response

                else:
                    return None
            else:
                return (Error("From or To node not found."))
        else:
            return (Error("Graph not found."))

    def _find_all_paths(self,graph_name, current_node, target_node, visited, path, paths):
        """
        Helper method to find all paths between two nodes
        """
        visited.add(current_node)
        path.append(current_node)
        if current_node == target_node:
            paths.add(tuple(path))
        else:
            for edge in self.graph_des[graph_name]:
                if edge.from_node == current_node and edge.to_node not in visited:
                    self._find_all_paths(graph_name, edge.to_node, target_node, visited, path, paths)
        path.pop()
        visited.remove(current_node)


if __name__ == "__main__":
    print("Running Client.py")
