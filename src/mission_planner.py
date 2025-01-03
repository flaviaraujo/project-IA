# The class MissionPlanner is responsible for planning the mission.
# Calls the search algorithms and returns the best path for each vehicle,
# considering the supplies and catastrophes in the environment.
# It holds the following camps:
# - graph:        graph of the environment
# - catastrophes: dictionary of catastrophes where the key is the node name
# - fleet:        dictionary of vehicles     where the key is the node name
# - supplies:     dictionary of supplies     where the key is the node name

from graph.graph import Graph
from algorithms  import (
    bfs,
    dfs,
    ucs,
    greedy,
    astar
)

from operation import operation_order

import copy
import json


class MissionPlanner:
    def __init__(self, graph: Graph, catastrophes: dict,
                 fleet: dict, supplies: dict):
        self.graph = graph
        self.catastrophes = catastrophes
        self.fleet = fleet
        self.supplies = supplies
        self.backup = self.backup()

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
    # Object backup and restore methods
    ###
    def backup(self):
        return copy.deepcopy(self)

    def restore(self):
        self.graph = self.backup.graph
        self.catastrophes = self.backup.catastrophes
        self.fleet = self.backup.fleet
        self.supplies = self.backup.supplies

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

    # Currently not used
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
                return dfs.search
            case "ucs":
                return ucs.search
            case "greedy":
                return greedy.search
            case "astar":
                return astar.search
            case _:
                raise ValueError(f"Invalid search algorithm: {algorithm}")

    ###
    # Search methods
    ###
    def build_catastrophe_vehicles(self, search_algorithm, start_time=0):
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

        return catastrophe_vehicles

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
            vehicle, operations, fuel_consumption = available_vehicles.pop(0)

            # Store the vehicle and its operations to resolve the catastrophe
            vehicles_operations[catastrophe_key] = {
                "vehicle": vehicle,
                "operations": operations,
                "fuel_consumption": fuel_consumption
            }

            # Assign the objective to the vehicle as well as the operations
            vehicle.objective  = catastrophe_key
            vehicle.operations = operations

            # Remove the selected vehicle from all catastrophe options
            for key, vehicles in catastrophe_vehicles.items():
                # Update the list for the current catastrophe, removing the selected vehicle
                catastrophe_vehicles[key] = [v for v in vehicles if v[0].name != vehicle.name]

            # Resort the catastrophe keys based on updated vehicle counts
            sorted_catastrophe_keys = sorted(catastrophe_vehicles.keys(),
                                             key=lambda k: len(catastrophe_vehicles[k]))

        return vehicles_operations

    def planner(self, verbose: bool, algorithm: str):

        # Get the search algorithm
        try:
            search_algorithm = self.get_search_algorithm(algorithm)
        except ValueError as e:
            print(e)
            return

        # Define the structure to store the vehicles that
        # can reach the catastrophes in time
        # (Key: Catastrophe node, Value: (Vehicle, Operations, Fuel consumption))
        catastrophe_vehicles = self.build_catastrophe_vehicles(search_algorithm)

        if verbose:
            # Semi-serialize the catastrophe_vehicles
            catastrophe_vehicles_serialized = {
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
            print(json.dumps(catastrophe_vehicles_serialized, indent=4))

        # Find the optimal objective for each vehicle
        vehicles_operations = self.assign_optimal_objectives(catastrophe_vehicles, self.fleet)

        if verbose:
            vehicles_operations_serialized = {
                node: {
                    "vehicle": vehicle["vehicle"].name,
                    "operations": [str(operation) for operation in vehicle["operations"]],
                    "fuel_consumption": vehicle["fuel_consumption"]
                }
                for node, vehicle in vehicles_operations.items()
            }

            print("\nVehicles elected for each catastrophe:")
            print(json.dumps(vehicles_operations_serialized, indent=4))

        # Get and sort the operations by time and in case of tie by the operation type order
        operations = sum((v["operations"] for v in vehicles_operations.values()), [])
        operations = sorted(operations, key=lambda x: (x.time, operation_order[x.operation_type]))

        # Execute the operations by time oreder and update the state
        # Checks for destructive nodes and edges and updates the graph
        # TODO execute the operations and update the state
        time = 0
        operations_executed = []
        while True:
            # Check for destructive nodes
            nodes_to_destroy = [
                node
                for node, destruction_time in self.graph.destructive_nodes.items()
                if destruction_time == time
            ]

            # Destroy the nodes and update the graph
            for node in nodes_to_destroy:
                self.graph.destroy_node(node)

            # Check for destructive edges
            edges_to_destroy = [
                (node1, node2)
                for (node1, node2), destruction_time in self.graph.destructive_edges.items()
                if destruction_time == time
            ]

            # Destroy the edges and update the graph
            for node1, node2 in edges_to_destroy:
                self.graph.destroy_edge(node1, node2)

            # If the graph was updated, recompute the accessible nodes by the vehicles as well
            # as the objective catastrophes for each vehicle
            if nodes_to_destroy or edges_to_destroy:
                # Rebuild the catastrophe_vehicles
                catastrophe_vehicles = \
                    self.build_catastrophe_vehicles(search_algorithm, time)

                # Find the optimal objective for each vehicle
                vehicles_operations = \
                    self.assign_optimal_objectives(catastrophe_vehicles, self.fleet)

                # Get and sort the operations by time and in case of tie by the operation type order
                operations = sum((v["operations"] for v in vehicles_operations.values()), [])
                operations = sorted(operations, key=lambda x: (x.time, operation_order[x.operation_type]))

            # Get the operations that should be executed
            current_operations = [op for op in operations if op.time == time]

            # Execute the operations
            # TODO Update the state by executing the operations
            for operation in current_operations:
                print(operation)
                operations_executed.append(operation)
                # TODO
                # When a vehicle resolves a catastrophe find the next catastrophe to resolve
                # Repeat until there are no more catastrophes to resolve or the time is over

            # Check if all catastrophes were resolved
            if all(c.is_resolved() for c in self.catastrophes.values()):
                print(f"[{str(time).rjust(3)}] All catastrophes were resolved.")
                break

            # Check if the time to response to all catastrophes is over
            if all(c.has_time_expired(time) for c in self.catastrophes.values()):
                print(f"[{str(time).rjust(3)}] Time to response to all catastrophes is over.")
                break

            # Increment the time
            time += 1

        # Print the operations executed ordered by vehicle instead of time if the user wants it
        try:
            user_input = input("Print the operations executed ordered by vehicle? [Y/n]: ")
        except (KeyboardInterrupt, EOFError):
            print("\n")

        if user_input.lower() in {"", "y", "yes"}:
            operations_executed_by_vehicle = {}
            for operation in operations_executed:
                if operation.vehicle not in operations_executed_by_vehicle:
                    operations_executed_by_vehicle[operation.vehicle] = []

                operations_executed_by_vehicle[operation.vehicle].append(operation)

            for vehicle, operations in operations_executed_by_vehicle.items():
                print(f"\nVehicle {vehicle} operations:")
                for operation in operations:
                    print(operation)

        # Restore mission planner state after running the planner/simulator
        self.restore()
