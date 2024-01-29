"""Client Implementation"""

import json
import os
import sys

from client import ClientGraph, Error

class Client:
    """
    Client class
    """
    def __init__(self):
        """
        Constructor
        """
        self.graph_component = ClientGraph()


    def parse_json(self, json_file_path):
        """Method to parse the json file

        Args:
            json_file_path (str): Path to the json file
        """

        script_dir = os.getcwd()
        absolute_path = os.path.join(script_dir, json_file_path)

        with open(absolute_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        for graph_description in data:
            description = graph_description.get('tag')

            if description == "graph":
                graph_name = graph_description.get('name')
                edges = graph_description.get('edges')
                self.graph_component.graph(graph_name, edges)

            elif description == "join":
                source_graph = graph_description.get('add')
                destination_graph = graph_description.get('to')
                self.graph_component.join(source_graph, destination_graph)

            elif description == "path":
                source_node = graph_description.get('from')
                target_node = graph_description.get('to')
                self.graph_component.check_for_path(source_node, target_node)

            else:
                print(Error('Invalid tag').to_dict())
                return


if __name__ == '__main__':
    client = Client()
    json_file_name = sys.argv[1]
    client.parse_json(json_file_name)
