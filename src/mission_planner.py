# The class MissionPlanner is responsible for planning the mission.
# Calls the search algorithms and returns the best path for each vehicle,
# considering the supplies and catastrophes in the environment.
# It holds the following camps:
# - graph:        graph of the environment
# - catastrophes: dictionary of catastrophes where the key is the node name
# - fleet:        dictionary of vehicles     where the key is the node name
# - supplies:     dictionary of supplies     where the key is the node name

from graph.graph import Graph
from vehicle     import Vehicle
from catastrophe import Catastrophe
from operation   import Operation
from algorithms  import (
    bfs,
    dfs,
    ucs,
    greedy,
    astar
)

import json


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

    def get_vehicle(self, vehicle_name: str):
        for vehicle in sum(self.fleet.values(), []):
            if vehicle.name == vehicle_name:
                return vehicle
        return None

    def get_search_algorithm(self, algorithm: str):
        match algorithm:
            case "bfs":
                return bfs.search
            case "dfs":
                return dfs.search     # TODO
            case "ucs":
                return ucs.search     # TODO
            case "greedy":
                return greedy.search  # TODO
            case "astar":
                return astar.search   # TODO
            case _:
                raise ValueError(f"Invalid search algorithm: {algorithm}")

    ###
    # Search methods
    ###
    def assign_optimal_objectives(self, catastrophe_vehicles, fleet):
        # store the vehicles lsit operations to resolve the catastrophe
        vehicles_operations = {}

        # sort the catastrophe_vehicles by the lenght of vehicles that can reach the catastrophe
        sorted_catastrophe_keys = sorted(catastrophe_vehicles.keys(),
                                         key=lambda k: len(catastrophe_vehicles[k]))

        # assign the vehicle with the least fuel consumption to each catastrophe
        for catastrophe_key in sorted_catastrophe_keys:

            # Get the list of available vehicles for this catastrophe
            available_vehicles = catastrophe_vehicles[catastrophe_key]

            # If no vehicles are available, skip this catastrophe
            if not available_vehicles:
                continue

            # Find the vehicle with the least fuel consumption
            vehicle_data = available_vehicles.pop(0)
            vehicle = vehicle_data["vehicle"]
            operations = vehicle_data["operations"]
            fuel_consumption = vehicle_data["fuel_consumption"]

            # Store the vehicle and its operations to resolve the catastrophe
            vehicles_operations[catastrophe_key] = {
                "vehicle": vehicle,
                "operations": operations,
                "fuel_consumption": fuel_consumption
            }

            # Get the vehicle object from the fleet
            vehicle_object = self.get_vehicle(vehicle)
            if not vehicle_object:
                print(f"ERROR: Vehicle {vehicle} not found in the fleet")
                continue

            # Assign the objective to the vehicle as well as the operations
            vehicle_object.objective  = catastrophe_key
            vehicle_object.operations = operations

            # Remove the selected vehicle from all catastrophe options
            for key, vehicles in catastrophe_vehicles.items():
                # Update the list for the current catastrophe, removing the selected vehicle
                catastrophe_vehicles[key] = [v for v in vehicles if v["vehicle"] != vehicle]

            # Resort the catastrophe keys based on updated vehicle counts
            sorted_catastrophe_keys = sorted(catastrophe_vehicles.keys(),
                                             key=lambda k: len(catastrophe_vehicles[k]))

        return vehicles_operations

    def planner(self, algorithm: str):

        # Get the search algorithm
        try:
            search_algorithm = self.get_search_algorithm(algorithm)
        except ValueError as e:
            print(e)
            return

        # Define the structure to store the vehicles that
        # can reach the catastrophes in time
        # (Key: Catastrophe node, Value: (Vehicle, Operations, Fuel consumption))
        catastrophe_vehicles = {}

        for catastrophe_node, catastrophe in self.catastrophes.items():
            catastrophe_response_time = catastrophe.time

            # Find the vehicles that can reach the catastrophe
            for vehicle_node, vehicles in self.fleet.items():

                for vehicle in vehicles or []:

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

        # Semi-serialize the catastrophe_vehicles structure to print it
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
        print("Catastrophe that can be reached in time by the vehicles:")
        print(json.dumps(catastrophe_vehicles, indent=4))

        # Find the optimal objective for each vehicle
        vehicles_operations = self.assign_optimal_objectives(catastrophe_vehicles, self.fleet)

        print("\nVehicles elected for each catastrophe:")
        print(json.dumps(vehicles_operations, indent=4))

        # Execute the operations and update the vehicle's state by time order
        # TODO

        # When a vehicle resolves a catastrophe find the next catastrophe to resolve
        # Repeat until there are no more catastrophes to resolve or the time is over
        # TODO
        pass
