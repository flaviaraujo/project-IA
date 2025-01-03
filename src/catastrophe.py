# The class Catastrophe is used to store the information of a catastrophe such as:
# - time: sensitive time of response
# - supplies_demand: dictionary with the supplies type and the amount needed
# - accessible_vehicles: list of vehicles that can respond to the catastrophe

from supply import Supply
from heapq import heappush, heappop
from vehicle import Vehicle

import copy


class Catastrophe:
    def __init__(self, time, supplies_demand):
        self.time = time
        self.supplies_demand = supplies_demand
        self.accessible_vehicles = []  # List of tuples (vehicle name, path, fuel consumption)

    def __str__(self):
        return (
            "{\n"
            f"  time_to_respond: {self.time},\n"
            f"  supplies_demand: {self.supplies_demand},\n"
            f"  accessible_vehicles: {self.accessible_vehicles}\n"
            "}"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            self.time == other.time and
            self.supplies_demand == other.supplies_demand
        )

    def __hash__(self):
        return hash((self.time, self.supplies_demand))

    def copy(self):
        return copy.deepcopy(self)

    def serialize(self):
        return {
            "time_to_respond": self.time,
            "supplies_demand": self.supplies_demand,
            "accessible_vehicles": self.accessible_vehicles
        }

    def decrease_time(self, time_passed):
        self.time -= time_passed

    def supply(self, cargo_contents: dict[str, Supply]) -> (dict[str, int], dict[str, Supply]):
        """
        Provides the demanded supplies and returns the remaining supplies in the vehicle
        and the amount of supplies provided to the catastrophe.

        Args:
        - cargo_contents (dict): A dictionary of the vehicle's supplies with their kinds as keys
          and `Supply` objects as values.

        Returns:
        - tuple:
            - dict: The updated cargo contents after fulfilling the demands.
            - dict: The amount of each supply kind that was provided.
        """
        remaining_cargo = cargo_contents.copy()  # Clone the input cargo contents
        cargo_supplied = {}  # Track what was supplied to the catastrophe

        for supply_kind, demand in self.supplies_demand.copy().items():
            if supply_kind in remaining_cargo:
                supply = remaining_cargo[supply_kind]
                provided = min(supply.amount, demand)

                # Update the catastrophe's demand
                self.supplies_demand[supply_kind] -= provided
                if self.supplies_demand[supply_kind] <= 0:
                    del self.supplies_demand[supply_kind]

                # Update the vehicle's supply amount
                supply.amount -= provided
                if supply.amount <= 0:
                    del remaining_cargo[supply_kind]

                # Track what was supplied
                cargo_supplied[supply_kind] = provided

        return cargo_supplied, remaining_cargo
    
    def find_acessible_vehicles(self, graph, catastrophe_node, vehicles, max_response_time):
        self.accessible_vehicles = []

        for vehicle in vehicles:
            travel_time, fuel_used, path = calculate_travel_time_and_fuel(graph, vehicle.current_node, catastrophe_node, vehicle)
            if travel_time <= max_response_time:
                self.accessible_vehicles.append((vehicle.name, path, fuel_used))
                
    def assign_vehicle_to_catastrophe(self):
        # Sort accessible vehicles by fuel consumption
        self.accessible_vehicles.sort(key=lambda v: v[2])

        if self.accessible_vehicles:
            # Get the vehicle with the least fuel consumption
            best_vehicle_name, path, fuel_consumption = self.accessible_vehicles[0]
            if best_vehicle_name:
                best_vehicle_name.assign_objective(self)
    
    
                

def calculate_travel_time_and_fuel(graph, start_node, end_node, vehicle):
    if isinstance(start_node, str):
        start_node = next((n for n in graph.nodes if n.name == start_node), None)

    if isinstance(end_node, str):
        end_node = next((n for n in graph.nodes if n.name == end_node), None)

    if start_node not in graph.nodes or end_node not in graph.nodes:
        return None, None, None

    # Priority queue for Dijkstra's algorithm
    priority_queue = [(0, 0, start_node, [])]  # (current_distance, current_fuel, current_node, path)
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0

    visited = set()

    while priority_queue:
        current_distance, current_fuel, current_node, path = heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        path = path + [current_node.name]

        if current_node == end_node:
            return current_distance, current_fuel, path

        for neighbor, (distance, speed_mult, travel_method, access_level) in graph.graph[current_node]:
            if not vehicle.is_travel_possible(travel_method, access_level):
                continue

            new_distance = current_distance + distance / vehicle.speed
            new_fuel = current_fuel + vehicle.calculate_fuel_needed(distance)

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heappush(priority_queue, (new_distance, new_fuel, neighbor, path))

    return float('inf'), float('inf'), []

def update_catastrophe_data(graph, catastrophes, vehicles):
    for node in graph.nodes:
        if node.catastrophe:
            node.catastrophe.accessible_vehicles = find_vehicles_for_catastrophe(graph, node, vehicles, node.catastrophe.time)