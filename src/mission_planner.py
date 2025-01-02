# The class MissionPlanner is responsible for planning the mission.
# Calls the search algorithms and returns the best path for each vehicle,
# considering the supplies and catastrophes in the environment.
# It holds the following camps:
# - graph:        graph of the environment
# - catastrophes: dictionary of catastrophes where the key is the node name
# - fleet:        dictionary of vehicles     where the key is the node name
# - supplies:     dictionary of supplies     where the key is the node name

from graph.graph import Graph
from algorithms import (
    bfs,
    dfs,
    ucs,
    greedy,
    astar
)


class MissionPlanner:
    def __init__(self, graph: Graph, catastrophes: dict,
                 fleet: dict, supplies: dict):
        self.graph = graph
        self.catastrophes = catastrophes
        self.fleet = fleet
        self.supplies = supplies

    def __str__(self):
        return (
            "MissionPlanner: {\n"
            f"  graph: {self.graph},\n"
            f"  catastrophes: {self.catastrophes},\n"
            f"  fleet: {self.fleet},\n"
            f"  supplies: {self.supplies}\n"
            "}"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            self.graph == other.graph
            and self.catastrophes == other.catastrophes
            and self.fleet == other.fleet
            and self.supplies == other.supplies
        )

    def __hash__(self):
        return hash((self.graph, self.catastrophes, self.fleet, self.supplies))

    ###
    # Serialize methods for pretty printing
    ###

    def serialize_catastrophes(self):
        return {
            node: catastrophe.serialize()
            for node, catastrophe in self.catastrophes.items()
        }

    def serialize_fleet(self):
        return {
            node: [vehicle.serialize() for vehicle in vehicles]
            for node, vehicles in self.fleet.items()
        }

    def serialize_supplies(self):
        return {
            node: {
                supply_kind: supply.serialize()
                for supply_kind, supply in supplies.items()
            }
            for node, supplies in self.supplies.items()
        }

    ###
    # Utility methods
    ###

    # Returns a list with all vehicles in the fleet
    def get_vehicles_list(self):
        return sum(self.fleet.values(), [])

    ###
    # Search methods
    ###
    def planner(self, algorithm: str):

        # Get the search algorithm function
        search_algorithm = None
        match algorithm:
            case "bfs":
                search_algorithm = bfs.search
            case "dfs":
                search_algorithm = dfs.search     # TODO
            case "ucs":
                search_algorithm = ucs.search     # TODO
            case "greedy":
                search_algorithm = greedy.search  # TODO
            case "astar":
                search_algorithm = astar.search   # TODO
            case _:
                raise ValueError(f"Invalid search algorithm: {algorithm}")

        # Define the structure to store the vehicles that
        # can reach the catastrophes in time
        # (Key: Catastrophe node, Value: List of vehicles)
        catastrophe_vehicles = {}

        for catastrophe_node, catastrophe in self.catastrophes.items():
            catastrophe_response_time = catastrophe.time

            # Find the vehicles that can reach the catastrophe
            for vehicle_node, vehicles in self.fleet.items():
                for vehicle in vehicles:

                    # Run the search algorithm
                    result = search_algorithm(self.graph, vehicle, catastrophe_response_time,
                                              vehicle_node, catastrophe_node)

                    # Check if the vehicle can not reach the catastrophe
                    if not result:
                        continue

                    # Unwrap the search algorithm result tuple
                    operations, fuel_consumption = result

                    # Add the search algorithm result tuple with the vehicle
                    if catastrophe_node not in catastrophe_vehicles:
                        catastrophe_vehicles[catastrophe_node] = []

                    catastrophe_vehicles[catastrophe_node].append(
                        (vehicle, operations, fuel_consumption)
                    )

        # TODO remove this
        # Semi-serialize the catastrophe_vehicles structure to print it
        import json
        catastrophe_vehicles = {
            node: [
                {
                    "vehicle": vehicle.name,
                    "operations": [str(operation) for operation in operations],
                    "fuel_consumption": fuel_consumption
                }
                for vehicle, operations, fuel_consumption in vehicles
            ]
            for node, vehicles in catastrophe_vehicles.items()
        }
        print(json.dumps(catastrophe_vehicles, indent=4))

        # Find the optimal objective for each vehicle
        # Find the path for each vehicle (call the respective search algorithm)
        #     Consider destructive nodes/edges
        #     When a vehicle resolves a catastrophe, check if it can help in other catastrophes
        #     (prioritize catastrophes without vehicles to help), if not return to base
        pass
