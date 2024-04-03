#!/usr/bin/env python

from copy import deepcopy
from flask import Flask, request, jsonify
from client import ClientGraph, Error
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    # open readme file and return the content
    with open('../README.md', 'r') as file:
        content = file.read()
    return content

def is_longer_than_20(name):
    # check if name is longer than 20 ascii characters
    name_ascii = ''.join([i for i in name if ord(i) < 128])
    return len(name_ascii) > 20

def edge_cost_to_string(edge_list):
    for edge in edge_list:
        edge.cost = str(edge.cost)
    return edge_list

def get_graph_details(graphname):
    graph_comp_dict = graph_component.__dict__
    low = graph_comp_dict.get('cost_interval').get(graphname)[0]
    high = graph_comp_dict.get('cost_interval').get(graphname)[1]
    edges = deepcopy(graph_comp_dict.get('graph_des')[graphname])

    # change cost of an edge in string format
    edges = edge_cost_to_string(edges)
    print('edges',edges)
    edges_list = []
    for edge in edges:
        edges_list.append(edge.__dict__)
    return {"low": str(low), "high": str(high), "edges": edges_list}

# post request to create a new graph
@app.route('/new', methods=['POST'])
def handle_new_request():
    data = request.get_json()
    # Process 'new' request
    low = data.get('low')
    high = data.get('high')
    name = data.get('name')

    if is_longer_than_20(name):
        return jsonify({"error": "Graph name should be at most 20 ascii characters"})

    res = graph_component.add_graph(low, high, name)
    print(f"res: {type(res)}")
    if type(res) == Error:
        return jsonify(res.to_dict())
    else:
        return jsonify(get_graph_details(name))


# post request to add an edge to the graph
@app.route('/add', methods=['POST'])
def handle_add_request():
    data = request.get_json()

    # Process 'add' request
    name = data.get('name')
    from_node = data.get('from')
    to_node = data.get('to')
    cost = data.get('cost')

    if is_longer_than_20(from_node) or is_longer_than_20(to_node):
        return jsonify({"error": "Node names should be at most 20 ascii characters"})

    res = graph_component.graph(name, from_node, to_node, cost)
    if type(res) == Error:
        return jsonify(res.to_dict())
    else:
        return jsonify(get_graph_details(name))


# post request to join two graphs
@app.route('/join', methods=['POST'])
def handle_join_request():
    data = request.get_json()
    # Process 'join' request
    graph_name1 = data[0]
    graph_name2 = data[1]
    res = graph_component.join(graph_name2, graph_name1)
    print('type of res',type(res))
    if type(res) == Error:
        return jsonify(res.to_dict())
    else:
        return jsonify(get_graph_details(graph_name1))


# get request to get the nodes of the graph
@app.route('/nodes/<graphname>', methods=['GET'])
def get_nodes(graphname):
    response = []
    try:
        nodes = graph_component.__dict__.get('adj_list_des')[graphname].keys()
        for node in nodes:
            response.append({"node": node})
    except KeyError:
        response = {"error": f"Graph {graphname} not found"}
    return jsonify(response)

# get request to get the edges of the graph
@app.route('/edges/<graphname>', methods=['GET'])
def get_edges(graphname):
    response = []
    try:
        edges = deepcopy(graph_component.__dict__.get('graph_des')[graphname])

        edges = edge_cost_to_string(edges)
        for edge in edges:
            response.append(edge.__dict__)
    except KeyError:
        response = {"error": f"Graph {graphname} not found"}
    return jsonify(response)

# get request to get the path
@app.route('/path/<graphname>/<n1>/<n2>', methods=['GET'])
def get_path(graphname, n1, n2):
    # request format = GET path/<GraphName>/<NN>/<NN>
    response = deepcopy(graph_component.check_for_path(graphname, n1, n2))

    if type(response) == Error:
        return jsonify(response.to_dict())
    else:
        response['edges'] = edge_cost_to_string(response['edges'])
        response['cost'] = str(response['cost'])
        response['edges'] = [edge.__dict__ for edge in response['edges']]
        return jsonify(response)


if __name__ == '__main__':
    graph_component = ClientGraph()
    app.run(port=5432, debug=True)
