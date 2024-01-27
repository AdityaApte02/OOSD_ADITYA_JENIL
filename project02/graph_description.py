"""
Graph Description Module
"""

import json

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

class GraphDescription:
    """
    GraphDescription class
    """
    def __init__(self):
        """
        Constructor
        """
        self.graph_des = {}

    def execute_command(self, command):
        """
        Execute the given command
        """
        command_data = json.loads(command)
        command_type = command_data.get("tag")

        if command_type == "graph":
            # Handle graph query
            graph_name = command_data.get("name")
            edges = command_data.get("edges")
            self.graph(graph_name, edges)
        elif command_type == "join":
            # Handle join query
            graph_to_add = command_data.get("add")
            graph_to_join = command_data.get("to")
            self.join(graph_to_add, graph_to_join)
        elif command_type == "path":
            # Handle path query
            source_node = command_data.get("from")
            target_node = command_data.get("to")
            self.path(source_node, target_node)
        else:
            print("Invalid command")

    def graph(self, name, edges):
        """
        Graph method
        """
        # if the graph name is already present in the graph_des object
        if name in self.graph_des:
            # error
            print(Error("Graph name already present").to_dict())
            return

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
            edge_description = EdgeDescription(from_node, to_node, cost)
            edge_descriptions.append(edge_description)

        self.graph_des[name] = edge_descriptions


    # print the graph_des object from name with edges
    def print_graph_des(self, name):
        """
        Print the graph_des object from name with edges
        """
        print("graph name: ", name)
        print("edges: ")
        for edges in self.graph_des.values():
            for edge in edges:
                print(edge.from_node, edge.to_node, edge.cost)
        print("end")

    def is_node_present(self, node):
        """
        Check if the inputted node is present in the graph_des object
        """
        for edges in self.graph_des.values():
            for edge in edges:
                if edge.from_node == node or edge.to_node == node:
                    return True
        return False

    def join(self, graph_to_add, graph_to_join):
        """
        Join method
        """
        # Ask for incorporation of one graph into another
        incorporation = input(f"Do you want to incorporate {graph_to_add} into {graph_to_join}?:")
        if incorporation.lower() in ['y', 'yes']:
            if graph_to_add in self.graph_des and graph_to_join in self.graph_des:
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
                else:
                    # extend the edge
                    self.graph_des[graph_to_join].extend(self.graph_des[graph_to_add])
                    # delete the graph_to_add from the graph_des object
                    del self.graph_des[graph_to_add]

                    # print graph_des
                    print(self.print_graph_des(graph_to_join))
            else:
                # error
                Error(f"{graph_to_add} or {graph_to_join} not found").to_dict()
        else:
            Error("Incorporation cancelled").to_dict()

    def is_path_present(self, source_node, target_node):
        """
        Check if there is a path between source_node and target_node
        """
        visited = set()
        stack = [source_node]

        while stack:
            node = stack.pop()
            visited.add(node)

            if node == target_node:
                return True

            for edges in self.graph_des.values():
                for edge in edges:
                    if edge.from_node == node and edge.to_node not in visited:
                        stack.append(edge.to_node)

        return False


    def path(self, source_node, target_node):
        """
        Path method
        """
        # if the source and target nodes are present in the graph
        if self.is_node_present(source_node) and self.is_node_present(target_node):
            # if there is a path from source to target
            # if self.is_path_present(source_node, target_node):
                # Construct the response dictionary
            response = {
                "tag": "cost",
                "edges": []
            }
            visited = set()
            stack = [(source_node, [])]

            while stack:
                node, path = stack.pop()
                visited.add(node)

                if node == target_node:
                    response["edges"].extend(path)
                    break

                for edges in self.graph_des.values():
                    for edge in edges:
                        if edge.from_node == node and edge.to_node not in visited:
                            stack.append((edge.to_node, path + [edge]))

            if response["edges"]:
                print(response)
                print(response["edges"][0].from_node)
                print(response["edges"][0].to_node)
                print(response["edges"][0].cost)
            else:
                print("null")
        else:
            print(Error("Source or target node not found").to_dict())


# GraphDescription =
#                     { "tag" : "graph", "name" : GraphName,  "edges" : [EdgeDescription, ...] }

#                  | { "tag" : "join",  "add"  : GraphName,  "to" : GraphName }

#                  | { "tag" : "path",  "from" : NodeName,   "to" : NodeName }


# initialize the GraphDescription object
test = GraphDescription()

# test the graph method
test.execute_command("""{"tag":"graph",
                        "name":"graph1",
                        "edges":[{"from_node":"a","to_node":"b", "cost": 2},
                                {"from_node":"b","to_node":"c", "cost":4},
                                {"from_node":"a","to_node":"c", "cost":3}]}""")

# test.execute_command("""{"tag":"graph",
#                         "name":"graph3",
#                         "edges":[{"from_node":"a","to_node":"b", "cost": 2},
#                                 {"from_node":"b","to_node":"c", "cost":3},
#                                 {"from_node":"c","to_node":"a", "cost":1},
#                                 {"from_node":"d","to_node":"b", "cost":6}]}""")


# test.execute_command('''{"tag":"graph",
#                      "name":"graph2",
#                      "edges":[{"from_node":"b","to_node":"a"},
#                               {"from_node":"b","to_node":"c", "cost":13}]}''')

test.execute_command('''{"tag":"graph",
                     "name":"graph2",
                     "edges":[{"from_node":"d","to_node":"e"},
                              {"from_node":"f","to_node":"e", "cost":13}]}''')

# test the join method
test.execute_command('{"tag":"join","add":"graph2","to":"graph1"}')

# test the path method
test.execute_command('{"tag":"path","from":"a","to":"c"}')

# print the graph_des object
# print(test.graph_des)

# test
# print(test.is_path_present("b","c"))