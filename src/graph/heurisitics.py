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

        for catastrophe_node in catastrophes.keys():
            heuristic_value[catastrophe_node] = {}

            for vehicle in vehicles:
                distance = graph.get_distance(node, catastrophe_node, vehicle)

                heuristic_value[catastrophe_node][vehicle.category] = distance

        graph.h[node.name] = heuristic_value


# Medium heuristic: 
# For each vehicle: distance + time_arrival_vehicle - time_response_catastrophe + fuel
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
                distance = graph.get_distance(node, catastrophe_node, vehicle)
                vehicle_time = (distance / vehicle.speed) * 60 - catastrophe.time
                vehicle_fuel = distance * vehicle.fuel_consumption / 100

                heuristic_value[catastrophe_node][vehicle.category] = \
                    distance + vehicle_time + vehicle_fuel

        graph.h[node.name] = heuristic_value


# Complex heuristic:
# For each vehicle : distance + time_arrival_vehicle - time_response_catastrophe + fuel + cargo
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
                distance = graph.get_distance(node, catastrophe_node, vehicle)
                vehicle_time = (distance / vehicle.speed) * 60 - catastrophe.time
                vehicle_fuel = distance * vehicle.fuel_consumption / 100
                cargo = vehicle.cargo_capacity - catastrophe.get_supplies_demand_amount()

                heuristic_value[catastrophe_node][vehicle.category] = \
                    distance + vehicle_time + vehicle_fuel + cargo

        graph.h[node.name] = heuristic_value
