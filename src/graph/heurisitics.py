# Heuristic format for a node A, where B and C are nodes with catastrophes:
"""
"A": {
    "B": {
        "motorcycle": 50,
        "car": 100,
        "truck": 200,
        (...)
    },
    "F": {
        "motorcycle": 100,
        "car": 200,
        "truck": infinity,
        (...)
    }
}
"""


# Simple heuristic:
# Distance between the node and each catastrophe for each vehicle.
def heuristic_fn1(params: dict) -> None:
    # Get the parameters
    graph        = params['graph']
    catastrophes = params['catastrophes']
    vehicles     = params['vehicles']

    # Update heuristic values for each node in the graph
    for node in graph.nodes:
        heuristic_value = {}

        for catastrophe_node, catastrophe in catastrophes.items():
            heuristic_value[catastrophe_node] = {}

            for vehicle in vehicles:
                distance = graph.get_distance(node, catastrophe_node, vehicle)
                heuristic_value[catastrophe_node][vehicle.category] = distance

        graph.h[node.name] = heuristic_value


# Medium heuristic:
# TODO
def heuristic_fn2(params: dict) -> None:
    # Get the parameters
    graph        = params['graph']
    catastrophes = params['catastrophes']
    vehicles     = params['vehicles']

    for node in graph.nodes:
        heuristic_value = {}

        for catastrophe_node, catastrophe in catastrophes.items():
            heuristic_value[catastrophe_node] = {}

            for vehicle in vehicles:
                # distance = graph.get_distance(node, catastrophe_node, vehicle)
                heuristic_value[catastrophe_node][vehicle.category] = 0

        graph.h[node.name] = heuristic_value


# Complex heuristic:
# TODO
def heuristic_fn3(params: dict) -> None:
    # Get the parameters
    graph        = params['graph']
    catastrophes = params['catastrophes']
    vehicles     = params['vehicles']

    for node in graph.nodes:
        heuristic_value = {}

        for catastrophe_node, catastrophe in catastrophes.items():
            heuristic_value[catastrophe_node] = {}

            for vehicle in vehicles:
                # distance = graph.get_distance(node, catastrophe_node, vehicle)
                heuristic_value[catastrophe_node][vehicle.category] = 0

        graph.h[node.name] = heuristic_value
